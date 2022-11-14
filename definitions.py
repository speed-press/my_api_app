import os

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

ENVIRONMENT = 'DEV'
APP_URL_PREFIX = '/v1'

PROD_CONFIG = 'config.config.ProdConfig'
DEV_CONFIG = 'config.config.DevConfig'
TEST_CONFIG = 'config.config.TestConfig'
DB_CONFIG = ROOT_DIR + '//config//db_config.ini'

# Log Files
ROOT_LOG_FILE = ROOT_DIR + '//logs//error.log'
ENDPOINT_LOG_FILE = ROOT_DIR + '//logs//endpoint.log'
QUERY_LOG_DIR = ROOT_DIR + '//logs//query.log'
DATA_LOG_DIR = ROOT_DIR + '//logs//data.log'

