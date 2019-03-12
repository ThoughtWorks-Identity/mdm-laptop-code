import logging
import logging.handlers
import requests
import datetime
import json
import SumologicHandler
import time


def logtoSumo(msg):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    host = 'host'
    url = 'url'
    http_handler = SumologicHandler.SumologicHandler(
        host,
        url,
        method='POST'
        )

    formatter = logging.Formatter('{\"Time\": %(asctime)s,\"name\": \"%(name)s\", \"Level\": \"%(levelname)s\", \"message\": \"%(message)s\"}', datefmt="%Y%m%d%H%M%S.000Z")
    formatter.converter = time.gmtime
    http_handler.setFormatter(formatter)
    logger.addHandler(http_handler)
    return logger.info(msg)


logtoSumo("trying new function")
#print(http_handler)
