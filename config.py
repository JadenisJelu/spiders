import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setlogger():
    log_formatter = logging.Formatter('%(asctime)s %(message)s')

    base = Path('.')

    logFile = base / 'log'

    my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=500*1024*1024, #500mb
                                    backupCount=2, encoding=None, delay=False)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.INFO)

    app_log = logging.getLogger(__name__)
    app_log.setLevel(logging.INFO)

    app_log.addHandler(my_handler)
    
    return app_log

if __name__ == '__main__':
    app_log = setlogger()
    for i in range(10**3):
        app_log.info(f"data: {i}")
