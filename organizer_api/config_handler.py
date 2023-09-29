import configparser
import os
import appdirs
from typing import List

class Config(configparser.ConfigParser):
    def __init__(self, config_directory:str = None, config_name_file:str = "organizer_config"):
        super().__init__()
        
        self.configdirectory = config_directory
        self.config_name_file = config_name_file
        
        if config_directory is None:
            self.configdirectory = appdirs.user_config_dir()
    
        if os.path.exists(os.path.join(self.configdirectory, self.config_name_file + ".ini")):
            self.read(os.path.join(self.configdirectory,  self.config_name_file + ".ini"))
        else:
            self.create_config()
    
    def reload(self):
        self.__init__()
    
    def create_config(self):
        if os.path.exists(os.path.join(self.configdirectory,  self.config_name_file + ".ini")) == False:
            self.add_section("initial_config")
            self.set("initial_config", "is_initial", str(True))
            with open(os.path.join(self.configdirectory, self.config_name_file + ".ini"), "w",  encoding="utf-8") as fp:
                self.write(fp)
    
    def save_config(self):
        with open(os.path.join(self.configdirectory, self.config_name_file + ".ini"), "w", encoding="utf-8") as fp:
            self.write(fp)
                
    def get_filters(self) -> List[str]:
        
        filters =[]
        all_sections = self.sections()
        
        for section in all_sections:
            if section.startswith("Filter"):
                filters.append(self.items(section)[0][1])
                
        return filters
        
            

    
    
    
