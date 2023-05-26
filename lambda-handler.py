import json
import urllib.parse
import boto3
import gzip
from datetime import datetime,timezone

import re, sys
import requests
import os
from util.albparser import parse_alb_log_line,parse_datetime,redact_qs
from destinations.influxdb import InlfuxDBDestinationHandler


s3 = boto3.client('s3')


def lambda_handler(event, context):
    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    s3.download_file(bucket, key, '/tmp/log.gz')
    # f = gzip.GzipFile("/tmp/log.gz","rb")
    with gzip.open('/tmp/log.gz','rt') as f:
      for line in f:
        # print('got line', line)
        log = parse_alb_log_line(line)
        InlfuxDBDestinationHandler.push(log)

