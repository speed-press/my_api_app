import time
from logging.handlers import TimedRotatingFileHandler


class MyRotatingFileHandler(TimedRotatingFileHandler):
    """ A rotating filehandler that adds the time as part of the file
        instead of appending it the end of the file.

        Old behavior: log.log2022-01-01
        New behavior: log_2022-01-01.log 
    """
    
    def __init__(
            self, filename, mode='a', backupCount=0, encoding=None, 
            delay=True, interval=1, when='MIDNIGHT'):
        super().__init__(
            filename=filename, when=when, 
            interval=interval, delay=delay)

        self.namer = self.addTimeToLog
        self.suffix = ''
    
    def addTimeToLog(self, logfile):

        if self.when == 'S':
            format = "%Y-%m-%d_%H-%M-%S"
        elif self.when == 'M':
            format = "%Y-%m-%d_%H-%M"
        elif self.when == 'H':
            format = "%Y-%m-%d_%H"
        elif self.when == 'D' or self.when == 'MIDNIGHT':
            format = "%Y-%m-%d"
        elif self.when.startswith('W'):
            format = "%Y-%m-%d"
        
         # Disables the suffix 
        t = time.strftime(format, time.localtime(self.rolloverAt))
        self.suffix = ''
        return logfile.replace('.log', f'_{t}.log')


