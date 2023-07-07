import re


def get_key_by_att(log, attribute):
    value = log.get(attribute)
    regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    if (re.search(regex, value)):
        key = "range-cidr"
    else:
        key = f"range-{attribute}"
    return key


def ipToCIDR(ip):
    separator = '.'
    result = ip.rsplit(separator, 1)[0]
    result += '.0/24'
    return result
