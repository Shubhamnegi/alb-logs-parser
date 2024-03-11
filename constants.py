import os

class ApplicationConstant():
   REDIS_HOST = os.environ.get('REDIS_HOST')
   REDIS_PORT = os.environ.get('REDIS_PORT')
   INVALID_PATHS = os.environ.get('INVALID_PATHS')
   INVALID_DOMAINS = os.environ.get('INVALID_DOMAINS')
   VALID_COUNTRY_LIST = os.environ.get('VALID_COUNTRY_LIST')