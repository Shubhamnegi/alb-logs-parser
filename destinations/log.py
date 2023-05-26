import logging
import sys
from destinations.DestinationHandler import DestinationHandler
import json
from util.albparser import redact_qs

class ConsoleDestinationHandler(DestinationHandler):
    @staticmethod
    def push(log:dict):
        # redact url
        url = log.get('request_url')
        log['escaped_url']= redact_qs(url)        
        
        print(json.dumps(log))