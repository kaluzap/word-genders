import pandas as pd
from pathlib import Path
from configuration import configuration

WORDS_KINDS = ["adjectives", "nouns", "verbs", "adverbs"]

class Dictionary():
    
    def __init__(self):
        self.data = pd.DataFrame()
        self.name = "missing dictionary"
        self.path = configuration.DATA_PATH
        self.kind = "unknown"
        self.language = "unknown"
        self.translation = "unknown"
        
    def load_dictionary(self, dictionary_path=None):
        if dictionary_path is None:
            dictionary_path = self.path
        try:
            self.data = pd.read_csv(dictionary_path)
        except FileNotFoundError:
            print(f'I cannot open the file "{dictionary_path}"')
            self.data = pd.DataFrame()
            return
        self.path = Path(dictionary_path)
        self.name = Path(dictionary_path).name
        self.data["active"] = True
        
        parameters = self.name.replace(".csv","")
        parameters = parameters.split("_")
        if len(parameters) >= 4:
            if parameters[1] in WORDS_KINDS:
                self.kind = parameters[1]
            self.language = parameters[2]
            self.translation = parameters[3]
        
        if "mistakes" not in self.data.columns:
            self.data["mistakes"] = 1
        self.data["p"] = 0
        
        print(f"Dict: {self.name}")
        print(f"Kind: {self.kind}")
        print(f"Lang: {self.language}")
        print(f"Tran: {self.translation}")
        print(self.data.head())
        
    def make_all_active(self):
        self.data["active"] = True
        print(
            f"There are {self.data[self.data['active']==True].shape[0]} words of {self.data.shape[0]}."
        )
        
    def save_dictionary(self):
        self.data.drop(columns=["active", "p"], inplace=True)
        self.data.to_csv(self.path, index=False, quoting=2)
        print(f"Saving dictionary {self.name}")
    
    
    
    
    
