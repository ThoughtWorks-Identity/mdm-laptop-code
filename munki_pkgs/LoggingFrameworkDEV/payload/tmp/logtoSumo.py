import logging
import logging.handlers
import SumologicHandler
import time
import os



def logtoSumo(serialNumber, msg):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    host = '{{ host }}'
    url = '{{ logging_dev_url }}'
    http_handler = SumologicHandler.SumologicHandler(
        host,
        url,
        method='POST'
        )
    serial_number = serialNumber
    formatter = logging.Formatter('{\"Time\": \"%(asctime)s\",\"name\": \"%(name)s\", \"Level\": \"%(levelname)s\", \"message\": \"%(message)s\",\"serial_number\": \"'+serial_number+'\"}')
    formatter.converter = time.gmtime
    http_handler.setFormatter(formatter)
    logger.addHandler(http_handler)
    return logger.info(msg)

#this is an example of how you can call this function...
#logtoSumo("C02RK1L3GTWS" ,"installation is started")
