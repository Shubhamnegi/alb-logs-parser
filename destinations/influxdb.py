import os
import requests
from destinations.DestinationHandler import DestinationHandler
from util.albparser import parse_datetime,redact_qs


INFLUX_DB_HOST = os.getenv("INFLUX_DB_HOST")
INFLUX_DB_USER = os.getenv("INFLUX_DB_USER")
INFLUX_DB_PASSWORD = os.getenv("INFLUX_DB_PASSWORD")

class InlfuxDBDestinationHandler(DestinationHandler):
    @staticmethod
    def push(log:dict):    
        data = f"alblog,type={log.get('type')},alb={log.get('alb')},alb_status_code={log.get('alb_status_code')},backend_status_code={log.get('backend_status_code')},request_verb={log.get('request_verb')},request_url={redact_qs(log.get('request_url'))},target_group_arn={log.get('target_group_arn')},domain_name={log.get('domain_name')} request_processing_time={log.get('request_processing_time')},backend_processing_time={log.get('backend_processing_time')},response_processing_time={log.get('response_processing_time')},received_bytes={log.get('received_bytes')},sent_bytes={log.get('sent_bytes')} {parse_datetime(log.get('timestamp'))}"
        response = requests.post(
            url=INFLUX_DB_HOST+f"/write?db=telegraf&u={INFLUX_DB_USER}&p={INFLUX_DB_PASSWORD}&precision=ms",
            data=data,
            headers={
            'Content-Type': 'application/octet-stream'
        })
        if(response.status_code > 201):
            print(response.status_code)
