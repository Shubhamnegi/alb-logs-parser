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
                return total_score, total_score
        return 0, total_score

    def threat_percentage(self):
        sum = 0
        total = 0
        match_score, total_score = self.threshold_breach()
        if match_score > 0:
            sum = sum + match_score
        total = total + total_score
        return sum/total * 100
