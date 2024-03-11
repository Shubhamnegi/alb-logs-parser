import json
from util.RateCalculator import RateCalculator
from util.ThreatCalculator import ThreatCalculator
from util.helper import get_country_from_IP,get_field_for_rate_calulation,get_key_by_att,ip_to_CIDR
import unittest


class TestRateCalculator(unittest.TestCase):
    sample_log = ''' 
    {
        "type": "https",
        "timestamp": "2023-07-06T07:39:57.795850Z",
        "alb": "app/k8s-limetrayalb-bd85f15f4e/f41667249a436f50",
        "client_ip": "112.215.18.82",
        "client_port": "54262",
        "backend_ip": "172.22.139.70",
        "backend_port": "8080",
        "request_processing_time": "0.001",
        "backend_processing_time": "0.001",
        "response_processing_time": "0.000",
        "alb_status_code": "201",
        "backend_status_code": "201",
        "received_bytes": "1617",
        "sent_bytes": "169",
        "request_verb": "POST",
        "request_url": "https://log-management-service.limetray.com:443/api/v1/web-pos/log/bulk",
        "request_proto": "HTTP/1.1",
        "user_agent": "-",
        "ssl_cipher": "ECDHE-RSA-AES128-GCM-SHA256",
        "ssl_protocol": "TLSv1.2",
        "target_group_arn": "arn:aws:elasticloadbalancing:ap-southeast-1:445897275450:targetgroup/k8s-producti-logmanag-607f2b2175/c30824a4b1aa06d0",
        "trace_id": "Root=1-64a66fcd-6d4979da4c1b3df979e7b573",
        "domain_name": "log-management-service.limetray.com",
        "chosen_cert_arn": "session-reused",
        "matched_rule_priority": "16",
        "request_creation_time": "2023-07-06T07:39:57.758000Z",
        "actions_executed": "waf,forward",        
        "escaped_url": "/api/v1/web-pos/log/bulk"
    }
    '''

    def pre_log_data(self):
        self.log = json.loads(self.sample_log)

    
    def test_calculate(self):        
        self.pre_log_data()
        fields = get_field_for_rate_calulation()
        self.log['ip_cidr_24'] = ip_to_CIDR(self.log['client_ip'])        
        assert self.log['ip_cidr_24'] == "112.215.18.0/24"
        for field in fields:
            attribute = field.get('field_name')
            timeout = field.get('exp')
            key = get_key_by_att(self.log,attribute)
            self.log[key] = RateCalculator.calculate(self.log, attribute, timeout)            
            print(f"key: {key} value: {self.log[key]} ")
            assert self.log[key] != None
        
                                
    
    def test_country_of_origin(self):
        self.pre_log_data()
        self.log['country_of_origin'] = get_country_from_IP(self.log.get('client_ip'))
        print(f'country of origin: {self.log["country_of_origin"]}')

        assert self.log['country_of_origin'] == "ID"

    def test_threat_caculator(self):
        self.pre_log_data()
        self.log['ip_cidr_24'] = ip_to_CIDR(self.log['client_ip'])        
        RateCalculator.process(self.log)

        tc = ThreatCalculator(self.log)
        threat_percentage = tc.calculate()
        print(self.log)
        print(threat_percentage, "threat_percentage")
        assert threat_percentage != None