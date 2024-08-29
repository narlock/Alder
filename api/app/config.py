import os
import yaml

# Import config.yaml into the project
def read_config(file_path):
    with open(file_path, 'r') as file:
        try:
            config = yaml.safe_load(file)
            return config
        except yaml.YAMLError as error:
            print(f"Error reading the YAML file: {error}")
            return None

# Configure to your configuration file
CONFIG = read_config('../alder/config.yaml')

MYSQL = CONFIG['mysql']
MYSQL_USER = MYSQL['user']
MYSQL_PASSWORD = MYSQL['password']
MYSQL_HOST = MYSQL['host']
MYSQL_DATABASE = MYSQL['database']

class Config:
#     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}')
    PYMYSQL_STRING = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}'
    print(PYMYSQL_STRING)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', PYMYSQL_STRING)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
