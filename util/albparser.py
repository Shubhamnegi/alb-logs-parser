import glob
from urllib.parse import parse_qsl, urlencode, urlparse
import maya
import re
import logging
import json


def parse_alb_log_line(line):
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
	regex = r"([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*):([0-9]*) ([^ ]*)[:-]([0-9]*) ([-.0-9]*) ([-.0-9]*) ([-.0-9]*) (|[-0-9]*) (-|[-0-9]*) ([-0-9]*) ([-0-9]*) \"([^ ]*) ([^ ]*) (- |[^ ]*)\" \"([^\"]*)\" ([A-Z0-9-\_]+) ([A-Za-z0-9.-]*) ([^ ]*) \"([^\"]*)\" \"([^\"]*)\" \"([^\"]*)\" ([-.0-9]*) ([^ ]*) \"([^\"]*)\" ($|\"[^ ]*\")(.*)"

	logDict = {}
	matches = re.search(regex, line)
	if matches:
		for i, field in enumerate(fields):
			# Create dict of fields and value
			logDict[field]=matches.group(i+1)
		# check of data is properly parsed	
		if(logDict.get('request_verb')!= None and logDict.get('request_verb') != ''):
			return logDict
		else:
			logging.error(f"error parsing log line {line}")
			return None
					
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

