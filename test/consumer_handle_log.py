import unittest
from dotenv import load_dotenv
load_dotenv()
import os
import logging
from pathlib import Path
from util.albparser import parse_alb_log_line


from util.LogsConsumer import LogsConsumer

class LogsConsumerTestCase(unittest.TestCase):
    required_fields = [
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
	]
    

    def test_hande_message(self):        
        json_file_path = Path.joinpath(Path.cwd(),'test/mock/mock.json')         
        # Read the JSON file
        with open(json_file_path, 'r') as file:
            json_data = file.read()            

        c = LogsConsumer(os.getenv('QUEUE_URL'))
        data = c.to_json(json_data)
        # 
        self.assertEqual('Records' in data, True) 
        bucket = c.get_s3_bucket(data)
        object_key = c.get_s3_object_key(data)

        self.assertEqual(bucket,"access-log-limetray-alb") 
        self.assertEqual(object_key,"AWSLogs/XXXX/elasticloadbalancing/ap-southeast-1/2023/05/24/445897275450_elasticloadbalancing_ap-southeast-1_app.k8s-limetrayalb-bd85f15f4e.f41667249a436f50_20230524T1125Z_18.143.212.16_4lmlz2ec.log.gz") 

        bucket_data = c.read_bucket_data(data)        
        for line in bucket_data:
            parsed_line = parse_alb_log_line(
                line.decode('utf-8'))
            logging.info(parsed_line)
            for field in self.required_fields:
                assert(field in parsed_line,True)
                assert(parsed_line[field]!="",True)
                

        

  
