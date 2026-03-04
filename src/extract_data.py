import os
from dotenv import load_dotenv
from pathlib import Path

import requests
import json
import logging


logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s  = %(message)s')

BASE_DIR = Path(__file__).resolve().parents[1]
env_path = BASE_DIR / "config" / ".env"

load_dotenv(env_path)

api_key = os.getenv('API_KEY')

print(api_key)

url = f'https://api.openweathermap.org/data/2.5/weather?q=Sao Paulo,BR&units=metrics&appid={api_key}'

def extract_weather_data(url : str) -> list:
    response = requests.get(url)
    data = response.json()
    
    print("Status code:", response.status_code)
    print("Response Text:", response.text)

    
    if response.status_code != 200:
        logging.error("Erro in request")
        
        return []
    
    if not data:
        logging.error("None data returned")
        
    output_path= 'data/waether_data.json'
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)
        
    return data


def extract_path_from_file(dir, filename):
    BASE_DIR = Path(__file__).resolve().parents[1]
    DATA_PATH = BASE_DIR / dir / filename
    
    return DATA_PATH

    
# extract_weather_data(url)