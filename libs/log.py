import logging
import logging.handlers
from pprint import pprint
import json
import time
import os.path
from config.settings import settings

if (settings['log_level']==1):
    LOG_LEVEL = logging.INFO
elif (settings['log_level']==2):
    LOG_LEVEL = logging.ERROR
elif (settings['log_level']==3):
    LOG_LEVEL = logging.WARNING    
else:
    LOG_LEVEL = logging.NOTSET     
    
timeTuple = time.localtime()
logsuffix = "%Y-%m-%d"+'.log'
LOG_FILENAME = 'run/logs/'+time.strftime(logsuffix, timeTuple)

logger = logging.getLogger(__name__)
#hdlr = logging.FileHandler(LOG_FILENAME)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#hdlr.setFormatter(formatter)
#logger.addHandler(hdlr)

#handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME,when='H',interval=1, backupCount=24)
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME,when='S',interval=10, backupCount=24)
handler.suffix = "%Y-%m-%d %H:%M:%S"+'.log' # or anything else that strftime will allow
handler.setFormatter(formatter)
handler.setLevel(LOG_LEVEL)
logger.addHandler(handler)

