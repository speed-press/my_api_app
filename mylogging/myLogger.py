import logging
from . import MyRotatingFileHandler


def myLogger(
        name, log_file=None, log_fmt=None, logfile_level=None, 
        stream_fmt=None, stream=False, stream_level=None, when='MIDNIGHT', 
        interval=10, propogate=True) -> logging.Logger:
    """    
    Create the different logger should you want a separate
    configuration for separate loggers. The log file handler 
    is initiated using the file_log__level.
    """
    if log_file == None and stream_level == None:
        raise('Logger must have a log file and/or stream level defined')

    logger = logging.getLogger(name)
    default_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Using the log_file file name as the indicator to set up the log to file
    # We expect most usage around not defining a custom formatter so we
    # check for the None first.
    if log_file:
        fh = MyRotatingFileHandler(
            filename=log_file, when=when, interval=interval)
        if log_fmt == None:
            fh.setFormatter(default_formatter)
        else:
            file_log_formatter = logging.Formatter(log_fmt)
            fh.setFormatter(file_log_formatter)
        logger.addHandler(fh)
    
    if stream:
        sh = logging.StreamHandler()
        if stream_level:
            sh.setLevel(getattr(logging, stream_level))
        else:
            if logfile_level == None:
                sh.setLevel(logging.ERROR)
            else:
                sh.setLevel(getattr(logging, logfile_level))
        if stream_fmt:
            stream_formatter = logging.Formatter(stream_fmt)
            sh.setFormatter(stream_formatter)
        else:
            sh.setFormatter(default_formatter)
        logger.addHandler(sh)
        
    if logfile_level:
        logger.setLevel(getattr(logging, logfile_level))
    else:
        logger.setLevel(logging.WARNING)
    if propogate == False:
        logger.propagate = False
    return logger
