from pathlib import Path
import json

# Paths
CONF_PATH = Path(__file__).parent.resolve()
DATA_PATH = (CONF_PATH / "../data").resolve()

SYS_DICTS = {"de":"sys_dict_de.cfg", "ru":"sys_dict_ru.cfg"}


class Configuration():
    
    def __init__(self, language="de"):
        self.sys_dict = {}
        self.path = CONF_PATH / SYS_DICTS[language]
        self.language = language
        self.load_configuration()
        
    def load_configuration(self, language=None):
        if language is not None:
            self.language=language
            self.path = CONF_PATH / SYS_DICTS[language]
        try:
            f = open(self.path)
        except FileNotFoundError:
            print(f'I cannot open the file "{self.path}"')
            self.data = pd.DataFrame()
            return
        print(f"loading {self.path}")
        self.sys_dict = json.load(f)


if __name__ == "__main__":

    print("\n")
    print("PATHS")
    print("=====")
    print(f"CONF_PATH = {CONF_PATH}")
    print(f"DATA_PATH = {DATA_PATH}")
    print("\n")
