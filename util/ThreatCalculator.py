
import json
import re
from util.helper import get_key_by_att
from util.helper import get_field_for_rate_calulation
from constants import ApplicationConstant


class ThreatCalculator():
    def __init__(self, log: dict) -> None:
        self.log = log
        self.match_score = 0
        self.total_score = 0

    def threshold_breach(self):
        weight = 2        
        fn_scored = 0

        attributes_list = get_field_for_rate_calulation()    
        if attributes_list == None:
            # exit if rate fields are not in env
            return 
        
        self.total_score += weight # update total score
        for att in attributes_list:
            if 'threshold' not in att:
                print(f'threshold does not exit in {att}')
                continue
            threshold = att['threshold']
            field = get_key_by_att(self.log, att['field_name'])
            value = self.log[field]
            
            attr_score = (int)(value)/(int)(threshold) * weight
            attr_score = attr_score if attr_score <= weight else weight # to keep max as weight
            fn_scored = attr_score if attr_score > fn_scored else fn_scored
        
        self.match_score = self.match_score + fn_scored
        
    def invalid_path_breach(self):
        invalid_path_list = ApplicationConstant.INVALID_PATHS
        if invalid_path_list == None:
            return
        
        self.total_score += 1
        attributes_list = json.loads(invalid_path_list)
        path = self.log['request_url']
        
        for regex in attributes_list:
            if (re.search(regex, path)):                
                self.match_score += 1
                break
            

    def no_user_agent(self):
        self.total_score += 1
        user_agent = self.log['user_agent']
        if (user_agent == "" or user_agent == "-"):            
            self.match_score += 1
        

    def invalid_domain(self):
        valid_domain = ApplicationConstant.INVALID_DOMAINS
        if valid_domain == None:
            return
        
        valid_domain = json.loads(valid_domain)
        self.total_score += 1
        
        domain = self.log['domain_name']
        if (re.search(valid_domain, domain)):            
            self.match_score += 1
        

    def invalid_country(self):
        countries = ApplicationConstant.VALID_COUNTRY_LIST
        if ('country_of_origin' in self.log and 
            self.log['country_of_origin'] not in countries):            
            self.match_score += 2
        self.total_score += 2

    def get_percentage(self):
        return round(self.match_score / self.total_score * 100,2) 

    def calculate(self):        
        self.threshold_breach()
        self.invalid_path_breach()
        self.no_user_agent()
        self.invalid_country()
        self.invalid_domain()        
        return self.get_percentage()        
