import pandas as pd
from pathlib import Path
from configuration import configuration


class Dictionary():
    
    def __init__(self):
        self.data = pd.DataFrame()
        self.name = "missing dictionary"
        self.path = configuration.DATA_PATH
        
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
        if "mistakes" not in self.data.columns:
            self.data["mistakes"] = 1
        self.data["p"] = 0
        print(self.data.head())
    
    
    
    
    
    
