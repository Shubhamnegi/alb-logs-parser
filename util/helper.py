import re
import maxminddb
import os
import json

def get_key_by_att(log, attribute):
    value = log.get(attribute)
    regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    if (re.search(regex, value)):
        key = "range-cidr"
    else:
        key = f"range-{attribute}"
    return key


def ip_to_CIDR(ip):
    separator = '.'
    result = ip.rsplit(separator, 1)[0]
    result += '.0/24'
    return result


def get_country_from_IP(ip):
    with maxminddb.open_database('database/dbip-country-lite-2023-07.mmdb') as reader:
        res = reader.get(ip)
        if 'country'  in res and  'iso_code' in res['country']:
            res = res['country']['iso_code']
            return res
        return ''

def get_field_for_rate_calulation():
    data = os.getenv('RATE_ATTRIBUTES')
    if data == None:
        return None
    fields = json.loads(data)
    return fields