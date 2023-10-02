import os
import pathlib
import shutil
from configparser import NoSectionError
from .config_handler import Config
from typing import List


class Filter:
    """
    Args:
        extensions (List[str]): extensions list.
        name (str): name of the filter.
        dir_output (str): directory output for move files by.
    
    """
    
    
    def __init__(self, extensions: List[str] = None, name: str = None, dir_output: str = None):
        self.extensions = extensions
        self.name = name
        self.dir_output = dir_output

        
        self.config = Config()
    
        if self.name is not None and self.is_not_none == False:
            self.load()
            

            
    #Guarda el filtro
    def save(self):
        if self.is_not_none():
            self.config[f"Filter.{self.name}"] = {
                "Name": self.name,
                "Extensions": self.extensions,
                "Directory": self.dir_output,
                }
            self.config.save_config()
   
            
    #Carga el filtro
    def load(self) -> bool:
        if self.name is not None:
            try:
                self.name = self.config.get(f"Filter.{self.name}", "Name")
                self.extensions = self.convert_to_list(self.config[f"Filter.{self.name}"]["Extensions"])
                self.dir_output = self.config.get(f"Filter.{self.name}", "Directory")
                
                return True
            except NoSectionError:
                raise Exception("Filter not found.")
            
    def delete(self):
        self.config.remove_section(f"Filter.{self.name}")
        self.config.save_config()

                
    def convert_to_list(self, string: str) -> List[str]:
        return string.strip("[]").strip('"').replace(" ", "").replace("'", "").split(",")

            
    def is_not_none(self) -> bool:
        return all(var is not None for var in [self.extensions, self.dir_output])

class File:
    """
    Args:
        path (str): The path where the files.
        name (str): The name of the file.
        extension (str): The extension of the file.
    
    """
    
    def __init__(self, path:str, name:str, extension: str):
        self.path = path
        self.name = name
        self.extension = extension

    def move(self, filter: Filter, actual_path) -> bool:
        actual = os.path.join(actual_path, filter.dir_output)
        
        if pathlib.Path(filter.dir_output).is_absolute() == True:
            if not os.path.isdir(filter.dir_output):
                if not os.path.exists(filter.dir_output):    
                    os.makedirs(filter.dir_output)
            
                else:
                    os.makedirs(filter.dir_output + "(organized)", exist_ok=True)
                    
                    shutil.move(self.path, filter.dir_output + "(organized)")
                    
                    return True
                
                    
            shutil.move(self.path, filter.dir_output)
            
            return True
        
        else:
            if not os.path.isdir(actual):
                if  not os.path.exists(actual):    
                    os.makedirs(actual)
            
                else:
                    os.makedirs(actual + "(organized)", exist_ok=True)
                    
                    shutil.move(self.path, actual + "(organized)")
                    
                    return True
                
                    
        shutil.move(self.path, actual)
            
        return True

    def delete(self):
        os.remove(os.path.join(self.path))
        
    @property
    def details(self) -> dict:
        self.detail = {
            "name": self.name,
            "path": self.path,
            "extension": self.name.split(".")[-1],
            "size": str(round((pathlib.Path(os.path.join(self.path)).stat().st_size / (1024 * 1024)), 2)) + "MB",   
        }
        
        return self.detail

class FileCollector:
    """
    Collects and manages files based on their path and extension.

    Args:
        path (str): The path where the files will be collected from.
        filter (Filter): The filter of the files by.

    Attributes:
        path (str): The path where the files will be collected from.
        filter (Filter): The filter of the files by.
        is_moved (bool): Indicates whether the files have been moved or not.
        files (list): The list of files found.
    """
    
    
    def __init__(self, path: str, filter: Filter):
        self.path = path
        self.filter = filter
        self.is_moved = False
        
        
    def filter_files(self) -> List[File]:
        list_files = []
        
        with os.scandir(self.path) as entries:
            for entry in entries:
                if entry.is_file():
                    for ext in self.filter.extensions:
                        if entry.name.split(".")[-1] == ext:
                            list_files.append(File(entry.path, entry.name, entry.name.split(".")[-1]))
        
        return list_files
        
        
    def move(self):
        if self.files:
            for file in self.files:
                file.move(self.filter, self.path)
            self.is_moved = True

    @property
    def files(self) -> List[File]:
        return self.filter_files()
    

def all_filters() -> List[Filter] | List:
    options = Config()
    filters_config = options.get_filters()
    if filters_config != []:
        return [Filter(name=filter) for filter in filters_config]
    return []