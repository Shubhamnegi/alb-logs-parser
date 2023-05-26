from util.ABSConsumer import ABSConsumer
import logging
import json
from util.s3helper import read_from_bucket
from util.albparser import parse_alb_log_line
from destinations.DestinationHandler import DestinationHandler

class LogsConsumer(ABSConsumer):
    
    def set_destination(self,destination_handler:DestinationHandler):
        self.destination_handler  = destination_handler

    def to_json(self,payload):        
        return json.loads(payload)
    
    def get_s3_bucket(self,payload):        
        """
        To get name of the bucket from which the event has raised
        """
        return payload['Records'][0]['s3']['bucket']['name']

    def get_s3_object_key(self,payload):        
        """
        To get key name which have been uploaded
        """
        return payload['Records'][0]['s3']['object']['key']

    def read_bucket_data(self,payload):        
        """
        to read data from bucket
        """
        bucket = self.get_s3_bucket(payload)
        object_key = self.get_s3_object_key(payload)
        data = read_from_bucket(bucket,object_key)
        return data
        

    def handle_message(self,payload):
        payload = self.to_json(payload)
        logging.info(f"LogsConsumer handler {payload}")        
        bucket_data = self.read_bucket_data(payload)        
        for line in bucket_data:
            parsed_line = parse_alb_log_line(
                line.decode('utf-8'))
            self.destination_handler.push(parsed_line)
            
            