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
df = (create_datafame(path_name))

def normalize_weather_columns(df):
    df_weather = pd.json_normalize(df['weather'].apply(lambda x : x[0]))
    
   
    
    df_weather = df_weather.rename(columns= {
        "id" : "weather_id",
        "main" : "weather_main",
        "description" : "weather_description",
        "icon" : 'weather_icon'
    })
    
    df = pd.concat([df, df_weather], axis = 1)
    
    logging.info(f"\n Column 'weather' was normalized - {len(df.columns)} column")

    return df

df = normalize_weather_columns(df)



def drop_column(df, columns_names):
    logging.info(f"Deleting the {columns_names} from {df.columns}")
    logging.info(f"Actual columns length from table: {len(df.columns)} ")
    df = df.drop(columns = columns_names)
    logging.info(f"Columns removed -  {len(df.columns)} remaining ")
    
    return df

df = drop_column(df, [])
