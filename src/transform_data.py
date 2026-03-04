import pandas as pd
from pathlib import Path
import json 
import logging
from extract_data import extract_path_from_file

logging.basicConfig(level = logging.INFO, format='%(asctime)s - %(levelname)s = %(message)s')



def create_datafame (path_name):
    logging.info(f'-> Criando DataFrame do arquivo JSON {path_name}')
    path = path_name

    
    if not path.exists():
        raise FileNotFoundError(f"File was not found{path}")
    
    with open(path) as json_f:
        data = json.load(json_f)
    
    logging.info(f'-> JSON file found and data created')
    
    return pd.json_normalize(data)



path_name = extract_path_from_file('data', 'weather_data.json') 
print(create_datafame(path_name))