import logging

from _logging.filehandler import MyRotatingFileHandler
from _logging.logger import Logger
from _logging.eLogger import elog
from definitions import (
    ROOT_LOG_FILE, 
    QUERY_LOG_DIR, 
    DATA_LOG_DIR, 
    ENDPOINT_LOG_FILE
)


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


endpoint_logger = Logger(
    name='endpoints', log_file=ENDPOINT_LOG_FILE, 
    logfile_level='DEBUG', stream=True, propogate=False)

query_logger = Logger(
    name='queries', log_file=QUERY_LOG_DIR, 
    logfile_level='DEBUG', stream=True, propogate=False)

data_logger = Logger(
    name='data', log_file=DATA_LOG_DIR, 
    logfile_level='DEBUG', stream=True, propogate=False)

