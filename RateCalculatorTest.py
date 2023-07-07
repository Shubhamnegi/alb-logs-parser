import json
import os
from util.rateCalculator import rateCalculator
import maxminddb
from util.ThreatCalculator import ThreatCalculator


class RateCalculatorTest():
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

    log = json.loads(sample_log)

    @classmethod
    def calculate(cls):
        data = os.getenv('attributes')
        fields = json.loads(data)
        for field in fields:
            attribute = field.get('field_name')
            timeout = field.get('exp')
            cls.log = rateCalculator(cls.log, attribute, timeout)

        tc = ThreatCalculator(cls.log)
        threat_percentage = tc.threat_percentage()
        print(threat_percentage, "threat_percentage")

    @classmethod
    def getCountryFromIP(cls):
        with maxminddb.open_database('database/dbip-country-lite-2023-07.mmdb') as reader:
            res = reader.get('125.63.125.210')
            res = res['country']['iso_code']
            print(res)


if __name__ == "__main__":
    RateCalculatorTest.calculate()
