import logging
import pandas as pd
from pathlib import Path
from typing import Optional
from configuration import configuration

# Setup Logger
logger = logging.getLogger(__name__)

# Standardized word categories
WORD_KINDS = ["adjectives", "nouns", "verbs", "adverbs"]

# Columns used for identifying unique words and sorting
KEY_COLUMNS = ["adjective", "adverb", "singular", "infinitive", "word", "plural"]

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
        self.data["active"] = True
        
        self._extract_metadata_from_name()
        
        if "mistakes" not in self.data.columns:
            self.data["mistakes"] = 1
        self.data["p"] = 0
        
        self._print_debug_info()

    def _extract_metadata_from_name(self) -> None:
        """Extracts kind, language, and translation from the filename."""
        # Expected format: data_[kind]_[lang]_[tran].csv
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
        """Saves the dictionary to CSV after deduplication and sorting."""
        if self.data.empty:
            return

        # Create a copy to avoid modifying the runtime state of self.data
        df_to_save = self.data.copy()
        
        # Remove internal runtime columns
        columns_to_drop = [c for c in ["active", "p"] if c in df_to_save.columns]
        df_to_save.drop(columns=columns_to_drop, inplace=True)
        
        # Deduplicate based on word columns
        subset = [c for c in KEY_COLUMNS if c in df_to_save.columns]
        df_to_save.drop_duplicates(subset=subset, inplace=True)
        
        # Sort by the primary word column
        if subset:
            df_to_save.sort_values(by=subset[0], inplace=True)
            
        df_to_save.to_csv(self.path, index=False, quoting=2)
        logger.info(f"Successfully saved dictionary: {self.name}")
