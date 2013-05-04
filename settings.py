from os import environ

TMP_DIR = './tmp'
FLASK_DEBUG = environ.get('ENV', 'development') == 'development'

LOCAL_ROOT = environ.get('LOCAL_ROOT', 'http://localhost:5000')
READMILL_CLIENT_ID = environ.get('READMILL_CLIENT_ID', 'dummy-client-id')
READMILL_CLIENT_SECRET = environ.get('READMILL_CLIENT_SECRET', 'dummy-client-secret')
READMILL_API_ROOT = 'https://api.readmill.com/v2'
READMILL_AUTH_URL = 'https://readmill.com/oauth/authorize'
READMILL_ACCESS_TOKEN_URL = 'https://readmill.com/oauth/token'

try:
  from local_settings import *
except ImportError:
  pass
