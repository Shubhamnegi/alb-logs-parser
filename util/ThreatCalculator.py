
import logging
import os
import time
import json
import redis
import re
from util.helper import get_key_by_att


class ThreatCalculator():
    def __init__(self, log: dict) -> None:
        self.log = log
        self.match_score = 0
        self.total_score = 0

    def threshold_breach(self):
        total_score = 2

        attributes_list_string = os.getenv('attributes')
        attributes_list = json.loads(attributes_list_string)

        for att in attributes_list:
            if 'threshold' not in att:
                print(f'threshold does not exit in {att}')
                continue
            threshold = att['threshold']
            field = get_key_by_att(self.log, att['field_name'])
            value = self.log[field]
            if (int)(threshold) <= (int)(value):
                print(
                    f'threshold breached for {field} where threshold is {threshold}')
                self.match_score += 2
            self.total_score += 2

    def invalid_path_breach(self):
        invalid_path_list = os.getenv('invalid_path')
        attributes_list = json.loads(invalid_path_list)

        for regex in attributes_list:
            path = self.log['request_url']
            if (re.search(regex, path)):
                print(f'invalid path for path {path}')
                self.match_score += 1
            self.total_score += 1

    def no_user_agent(self):
        user_agent = self.log['user_agent']
        if (user_agent == "" or user_agent == "-"):
            print('no user agent')
            self.match_score += 1
        self.total_score += 1

    def invalid_domain(self):
        valid_domain = os.getenv('valid_domain')
        domain = self.log['domain_name']
        if (re.search(valid_domain, domain) is False):
            print('invalid domain')
            self.match_score += 2
        self.total_score += 2

    def invalid_country(self):
        countries = os.getenv('country_list')
        if (self.log['country_of_origin'] not in countries):
            print('invalid country')
            self.match_score += 2
        self.total_score += 2

    def threat_percentage(self):
        sum = 0
        total = 0
        self.threshold_breach()
        self.invalid_path_breach()
        self.no_user_agent()
        self.invalid_country()
        self.invalid_domain()
        if self.match_score > 0:
            sum = sum + self.match_score
        total = total + self.total_score
        return sum/total * 100
