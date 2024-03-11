import logging
import redis
import re
from util.helper import get_key_by_att, ip_to_CIDR,get_field_for_rate_calulation
from  constants import ApplicationConstant


class RateCalculator():    

    @classmethod
    def process(cls,log:dict):
        fields = get_field_for_rate_calulation()
        for field in fields:
            attribute = field.get('field_name')
            timeout = field.get('exp')
            key = get_key_by_att(log,attribute)
            log[key] = cls.calculate(log, attribute, timeout)            
        return log
    
    @classmethod
    def calculate(cls,log: dict, attribute: str, timeout: int):
        r = redis.Redis(host=ApplicationConstant.REDIS_HOST,
                         port=ApplicationConstant.REDIS_PORT)
        
        value = log.get(attribute) # extract value from log
        key = get_key_by_att(log, attribute) # create redis key
        if ("cidr" in key):
            value = ip_to_CIDR(value) # if key has been transformed from client ip to cidr

        redis_key = f"alb::{key}::{value}" # Redis key for aggregation
        current = r.get(redis_key) # get current value from redis
        
        # TODO: move to singe transaction to remove conflict if more than 1 process is running.
        if (current != None):
            current = (int)(current)+1 # increment
            r.set(name=redis_key, value=current, ex=r.ttl(redis_key)) # update with remaining TTL
        else:
            current = 1 # init current
            timeout = (int)(timeout)  # Create new timeout 
            r.set(name=redis_key, value=current, ex=timeout) # update redis key, current, timeout        
        
        return current
