import logging
import pandas as pd
from pathlib import Path
from typing import Optional
from configuration import configuration

# Setup Logger
logger = logging.getLogger(__name__)

# Standardized word categories
WORD_KINDS = ["adjectives", "nouns", "verbs", "adverbs", "all"]

# Columns that identify a word. Each word appears once per dictionary, with
# all its translations in one row; the same spelling may only repeat with a
# different plural or gender (e.g. der See / die See).
KEY_COLUMNS = ["adjective", "adverb", "singular", "infinitive", "word", "plural", "gender"]

# Training scores live outside the dictionaries (and outside git), one row
# per dictionary and word: dictionary,word,score. Words with the default
# score are not stored.
SCORES_PATH = Path(configuration.DATA_PATH) / "scores.csv"
SCORES_COLUMNS = ["dictionary", "word", "score"]
DEFAULT_SCORE = 1

def merge_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Merges rows of the same word into one, joining their translations."""
    subset = [c for c in KEY_COLUMNS if c in df.columns]
    if not subset or not df.duplicated(subset=subset).any():
        return df

    def join_translations(values: pd.Series) -> str:
        if len(values) == 1:
            return values.iloc[0]
        parts = []
        for value in values.dropna():
            for part in str(value).split(","):
                part = part.strip()
                if part and part not in parts:
                    parts.append(part)
        return ", ".join(parts)

    aggregations = {c: "first" for c in df.columns if c not in subset}
    if "translation" in aggregations:
        aggregations["translation"] = join_translations
    if "mistakes" in aggregations:
        aggregations["mistakes"] = "max"

    repeated = df[df.duplicated(subset=subset)][subset].astype(str).agg("|".join, axis=1)
    logger.warning(f"Merged repeated words: {', '.join(sorted(set(repeated)))}")
    merged = df.groupby(subset, sort=False, as_index=False, dropna=False).agg(aggregations)
    return merged[df.columns]


class Dictionary:
    """
    Handles loading, managing, and saving word dictionaries stored in CSV format.
    """
    
    def __init__(self):
        self.data = pd.DataFrame()
        self.name = "missing dictionary"
        self.path = Path(configuration.DATA_PATH)
        self.kind = "unknown"
        self.language = "unknown"
        self.translation = "unknown"
        
    def load_dictionary(self, dictionary_path: Optional[str] = None) -> None:
        """Loads a dictionary from a CSV file and initializes metadata."""
        path_to_load = Path(dictionary_path) if dictionary_path else self.path
        
        try:
            self.data = pd.read_csv(path_to_load)
        except FileNotFoundError:
            logger.info(f'Error: Could not find dictionary at "{path_to_load}"')
            self.data = pd.DataFrame()
            return

        self.path = path_to_load
        self.name = path_to_load.name
        self.data = merge_duplicates(self.data)
        self.data["active"] = True
        
        self._extract_metadata_from_name()
        
        # Older dictionaries still carry a "mistakes" column; use it only for
        # words that have no entry in the scores file yet.
        legacy = self.data.pop("mistakes") if "mistakes" in self.data.columns else None
        scores = self._read_scores()
        mine = scores[scores["dictionary"] == self.name]
        mistakes = self._word_keys().map(dict(zip(mine["word"], mine["score"])))
        if legacy is not None:
            mistakes = mistakes.fillna(legacy)
        self.data["mistakes"] = mistakes.fillna(DEFAULT_SCORE).astype(int)
        self.data["p"] = 0
        
        self._print_debug_info()

    def _extract_metadata_from_name(self) -> None:
        """Extracts kind, language, and translation from the filename."""
        # Expected format: data_[kind]_[lang]_[tran].csv
        # Reset first so nothing is left over from the previous dictionary
        self.kind = self.language = self.translation = "unknown"
        parts = self.name.replace(".csv", "").split("_")
        if len(parts) >= 4:
            kind_candidate = parts[1]
            if kind_candidate in WORD_KINDS:
                self.kind = kind_candidate
            self.language = parts[2]
            self.translation = parts[3]

    def _print_debug_info(self) -> None:
        """Prints basic info about the loaded dictionary."""
        logger.info(f"Dict: {self.name}")
        logger.info(f"Kind: {self.kind}")
        logger.info(f"Lang: {self.language}")
        logger.info(f"Tran: {self.translation}")
        logger.info(self.data.head())
        
    def make_all_active(self) -> None:
        """Resets all words to active status."""
        self.data["active"] = True
        active_count = self.data["active"].sum()
        logger.info(f"Activated {active_count} of {len(self.data)} words.")
        
    def save_dictionary(self) -> None:
        """Saves the dictionary to CSV after merging repeated words and sorting."""
        if self.data.empty:
            return

        # Create a copy to avoid modifying the runtime state of self.data
        df_to_save = self.data.copy()
        
        # Remove internal runtime columns; scores are saved separately
        columns_to_drop = [c for c in ["active", "p", "mistakes"] if c in df_to_save.columns]
        df_to_save.drop(columns=columns_to_drop, inplace=True)
        
        df_to_save = merge_duplicates(df_to_save)
        subset = [c for c in KEY_COLUMNS if c in df_to_save.columns]
        
        # Sort by the primary word column
        if subset:
            df_to_save.sort_values(by=subset[0], kind="stable", inplace=True)
            
        df_to_save.to_csv(self.path, index=False, quoting=2)
        logger.info(f"Successfully saved dictionary: {self.name}")
        self.save_scores()

    def save_scores(self) -> None:
        """Writes this dictionary's scores to the scores file, keeping the
        entries of other dictionaries."""
        if self.data.empty:
            return

        scores = self._read_scores()
        others = scores[scores["dictionary"] != self.name]
        mine = pd.DataFrame({
            "dictionary": self.name,
            "word": self._word_keys(),
            "score": self.data["mistakes"].astype(int),
        })
        mine = mine[mine["score"] != DEFAULT_SCORE]

        result = pd.concat([others, mine]).sort_values(["dictionary", "word"], kind="stable")
        # Write to a temporary file first so a crash never leaves a half-written file
        tmp_path = SCORES_PATH.with_suffix(".tmp")
        result.to_csv(tmp_path, index=False)
        tmp_path.replace(SCORES_PATH)

    def _read_scores(self) -> pd.DataFrame:
        if not SCORES_PATH.exists():
            return pd.DataFrame(columns=SCORES_COLUMNS)
        return pd.read_csv(SCORES_PATH, dtype={"dictionary": str, "word": str}, keep_default_na=False)

    def _word_keys(self) -> pd.Series:
        """Identifies each word by its key columns, e.g. "Brand|Brände|m"."""
        subset = [c for c in KEY_COLUMNS if c in self.data.columns]
        return self.data[subset].astype(str).agg("|".join, axis=1)
