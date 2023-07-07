import logging
import os
import time
import json
import redis
import re
from util.ThreatCalculator import ThreatCalculator
from util.helper import get_key_by_att, ipToCIDR


def rateCalculator(log: dict, attribute: str, timeout: int):
    r = redis.Redis(host='cache', port=6379)
    value = log.get(attribute)
    key = get_key_by_att(log, attribute)
    if ("cidr" in key):
        value = ipToCIDR(value)

    redis_key = f"alb::{key}::{value}"
    current = r.get(redis_key)
    if (current != None):
        current = (int)(current)+1
        r.set(name=redis_key, value=current, ex=r.ttl(redis_key))
    else:
        current = 1
        timeout = (int)(timeout)
        r.set(name=redis_key, value=current, ex=timeout)
    log[key] = current
    print(log)
    return log
