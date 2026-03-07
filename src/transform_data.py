import pandas as pd
import json 
import logging
from extract_data import extract_path_from_file

logging.basicConfig(level = logging.INFO, format='%(asctime)s - %(levelname)s = %(message)s')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

columns_names_to_rename = {
        "base": "base",
        "visibility": "visibility",
        "dt": "datetime",
        "timezone": "timezone",
        "id": "city_id", 
        "name": "city_name",
        "coord.lon": "longitude",
        "coord.lat": "latitude",
        "main.temp": "temperature",
        "main.feels_like": "feels_like",
        "main.temp_min": "temp_min",
        "main.temp_max": "temp_max",
        "main.pressure": "pressure",
        "main.humidity": "humidity",
        "main.sea_level": "sea_level",
        "main.grnd_level": "grnd_level",
        "wind.speed": "wind_speed",
        "wind.deg": "wind_deg",
        "wind.gust": "wind_gust",
        "clouds.all": "clouds", 
        "sys.type": "sys_type",                 
        "sys.id": "sys_id",                
        "sys.country": "country",                
        "sys.sunrise": "sunrise",                
        "sys.sunset": "sunset",
        # weather_id, weather_main, weather_description 
    }
column_to_drop = ['weather', 'sys.type', 'weather_icon']
column_to_datetime = ['sunrise', 'sunset', 'datetime']

def create_datafame (path_name):
    logging.info(f'-> Criando DataFrame do arquivo JSON {path_name}')
    path = path_name

    
    if not path.exists():
        raise FileNotFoundError(f"File was not found{path}")
    
    with open(path) as json_f:
        data = json.load(json_f)
    
    logging.info(f'-> JSON file found and data created')
    
    return pd.json_normalize(data)


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


def drop_column(df, columns_names):
    logging.info(f"Deleting the {columns_names} from {df.columns}")
    logging.info(f"Actual columns length from table: {len(df.columns)} ")
    df = df.drop(columns = columns_names)
    logging.info(f"Columns removed -  {len(df.columns)} remaining ")
    
    return df


def rename_column(df, rename_columns):
    logging.info(f"Changing the column - {column_to_drop}")
    df = df.rename(columns = rename_columns)
    logging.info("Columns were changed")
    return df

def normalize_datetime_columns(df, columns_names):
    for name in columns_names:
        df[name] = pd.to_datetime(df[name], unit='s', utc=True).dt.tz_convert('America/Sao_Paulo')
        
    return df



def data_transformations():
    path = extract_path_from_file('data', 'weather_data'.json)
    df = create_datafame(path)
    df = normalize_weather_columns(df)
    df = drop_column(df, column_to_drop)
    df = rename_column(df, columns_names_to_rename)
    df = normalize_datetime_columns(df, column_to_datetime)
    
    logging.info('Transformações concluídas')
    return df