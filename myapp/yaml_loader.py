""" Yaml loader. In case we wanted to use yaml instead of configs"""
import yaml
from definitions import ROOT_DIR

DB_CONFIG_FILE = ROOT_DIR + '\\config\\database.yaml'
with open(DB_CONFIG_FILE, 'r') as tmp:
    config = yaml.full_load(tmp)

HOST = config['store_dev']['host']
USER = config['store_dev']['user']
PSW = config['store_dev']['psw']
PORT = config['store_dev']['port']
DATABASE = config['store_dev']['database']

AUTH_TABLE = config['auth']['authkeys']
AUTH_DB = config['auth']['database']