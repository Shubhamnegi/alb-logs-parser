#!/usr/bin/env python3
# coding=utf8
#
# AUTHOR: shubham negi <shubham16negi@gmail.com>
# Goal: To parse alb logs and push to influx db for analyzing
#

from ast import arg
import re, sys
import requests
import os
import maya
from urllib.parse import parse_qsl, urlencode, urlparse
import argparse
import glob


INFLUX_DB_HOST = os.getenv("INFLUX_DB_HOST")
INFLUX_DB_USER = os.getenv("INFLUX_DB_USER")
INFLUX_DB_PASSWORD = os.getenv("INFLUX_DB_PASSWORD")

def parse_alb_log_file(file_path):
	print(f"parsing logs at {file_path}")
	fields = [
		"type",
		"timestamp",
		"alb",
		"client_ip",
		"client_port",
		"backend_ip",
		"backend_port",
		"request_processing_time",
		"backend_processing_time",
		"response_processing_time",
		"alb_status_code",
		"backend_status_code",
		"received_bytes",
		"sent_bytes",
		"request_verb",
		"request_url",
		"request_proto",
		"user_agent",
		"ssl_cipher",
		"ssl_protocol",
		"target_group_arn",
		"trace_id",
		"domain_name",
		"chosen_cert_arn",
		"matched_rule_priority",
		"request_creation_time",
		"actions_executed",
		"redirect_url",
		"new_field",
	]
	# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.
	# REFERENCE: https://docs.aws.amazon.com/athena/latest/ug/application-load-balancer-logs.html#create-alb-table
	regex = r"([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*):([0-9]*) ([^ ]*)[:-]([0-9]*) ([-.0-9]*) ([-.0-9]*) ([-.0-9]*) (|[-0-9]*) (-|[-0-9]*) ([-0-9]*) ([-0-9]*) \"([^ ]*) ([^ ]*) (- |[^ ]*)\" \"([^\"]*)\" ([A-Z0-9-]+) ([A-Za-z0-9.-]*) ([^ ]*) \"([^\"]*)\" \"([^\"]*)\" \"([^\"]*)\" ([-.0-9]*) ([^ ]*) \"([^\"]*)\" ($|\"[^ ]*\")(.*)"

	with open(file_path, 'r') as file:
		for line in file:
			print(line)
			logDict = {}
			matches = re.search(regex, line)
			if matches:
				for i, field in enumerate(fields):
					# Create dict of fields and value
					logDict[field]=matches.group(i+1)
				# check of data is properly parsed	
				if(logDict.get('request_verb')!= None and logDict.get('request_verb') != ''):
					print('data parsed')
					# print(json.dumps(logDict))
					if(INFLUX_DB_HOST!= None and INFLUX_DB_HOST != ''):
						push_to_influx(logDict)
						# redact_qs(logDict.get('request_url'))
					else:
						print('db host not defined')
						break
				else:
					print('parsing failed')	
					
def parse_datetime(timestamp):
	# sample: 2022-03-18T23:57:23.204731Z
	date_time_obj = maya.parse(timestamp).datetime()
	return int(date_time_obj.timestamp()*1000)
	
	


def redact_qs(url):
	# to remove query string from path to reduce unique requests
	u = urlparse(url)
	## inlux is not supporting query string for somereason
	# parsed_query = dict(parse_qsl(u.query))
	# for k in parsed_query.keys():
	# 	parsed_query[k]="#"
	# redacted_query_string = urlencode(parsed_query)	
	# redactedurl=f"{u.scheme}://{u.netloc}{u.path}?{redacted_query_string}"
	redactedurl=f"{u.scheme}://{u.netloc}{u.path}"
	return redactedurl


	
	

def push_to_influx(log):    
    data = f"alblog,type={log.get('type')},alb={log.get('alb')},alb_status_code={log.get('alb_status_code')},backend_status_code={log.get('backend_status_code')},request_verb={log.get('request_verb')},request_url={redact_qs(log.get('request_url'))},target_group_arn={log.get('target_group_arn')},domain_name={log.get('domain_name')} request_processing_time={log.get('request_processing_time')},backend_processing_time={log.get('backend_processing_time')},response_processing_time={log.get('response_processing_time')},received_bytes={log.get('received_bytes')},sent_bytes={log.get('sent_bytes')} {parse_datetime(log.get('timestamp'))}"
    response = requests.post(
        url=INFLUX_DB_HOST+f"/write?db=telegraf&u={INFLUX_DB_USER}&p={INFLUX_DB_PASSWORD}&precision=ms",
        data=data,
        headers={
        'Content-Type': 'application/octet-stream'
    })
    if(response.status_code > 201):
    	print(response.status_code)
    


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description=f"To parse alb logs and push to influx at {INFLUX_DB_HOST}",prog='PROG',usage=f"{sys.argv[0]} --file file_name")
	parser.add_argument('-d','--dir', help='Logs directory Example: --dir log dir for logs')
	parser.add_argument('-f','--file', help='Log file path Example: --file file_path')
	args = parser.parse_args()
	
	if len(sys.argv) < 3:
		sys.exit(parser.print_help())
	
	if (args.dir != None):
		# diretory provived, will be parsing directory and searching for logs		
		try:
			files = os.listdir(args.dir)
			for f in files:
				filepath = f"{args.dir}/{f}"
				parse_alb_log_file(filepath)
		except NotADirectoryError as err:
			print(f"Invalid directory |  Error: {err}")
		except BaseException as err:
			print(f"Error: {err}")


	else:
		# file path provided will be parsing file directly		
		parse_alb_log_file(args.file)		