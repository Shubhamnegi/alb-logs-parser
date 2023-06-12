import unittest
from util.albparser import parse_alb_log_line,fix_domain_name
class ParseAlbLogLine(unittest.TestCase):
    mocklogline = 'http 2023-06-11T23:55:01.663125Z app/k8s-orderonlinealb-16f0d27f77/dbb741d995455ae5 50.0.21.104:53178 172.22.130.99:80 0.001 0.068 0.000 200 200 125 395 "POST http://engage-service.limetray.infra:80/crm/crons/send-repeat-instances HTTP/1.1" "curl/7.61.1" - - arn:aws:elasticloadbalancing:ap-southeast-1:445897275450:targetgroup/k8s-producti-dashboar-5889a48dce/f3858aa06f8eceda "Root=1-64865ed5-497db3947cd6881230e79f29" "-" "-" 6 2023-06-11T23:55:01.594000Z "waf,forward" "-" "-" "172.22.130.99:80" "200" "-" "-"'
    

    def testParseLogLing(self):
        logDict = parse_alb_log_line(self.mocklogline)        
        print(logDict)
        assert(logDict.get('domain_name') == 'engage-service.limetray.infra')
        