import logging

from .filehandler import MyRotatingFileHandler
from .myLogger import myLogger
from definitions import (
    ROOT_LOG_FILE, QUERY_LOG_DIR, 
    DATA_LOG_DIR, ENDPOINT_LOG_FILE)


###################################################################
# Setting default logging
###################################################################
fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
default_formatter = logging.Formatter(fmt)
fileHandler = MyRotatingFileHandler(filename=ROOT_LOG_FILE)
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(default_formatter)
streamHandler.setLevel(logging.ERROR)
logging.basicConfig(
    level=logging.ERROR, handlers=[fileHandler, streamHandler])

###################################################################
# Setting up loggers various purposes to separate specific information
###################################################################


endpoint_logger = myLogger(
    name='endpoint', log_file=ENDPOINT_LOG_FILE, 
    logfile_level='DEBUG', stream=True, propogate=False)

query_logger = myLogger(
    name='query', log_file=QUERY_LOG_DIR, 
    logfile_level='DEBUG', stream=True, propogate=False)

data_logger = myLogger(
    name='data', log_file=DATA_LOG_DIR, 
    logfile_level='DEBUG', stream=True, propogate=False)

