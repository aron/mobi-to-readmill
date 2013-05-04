from os import environ

TMP_DIR = './tmp'
FLASK_DEBUG = environ.get('ENV', 'development') == 'development'

LOCAL_ROOT = 'http://localhost:5000'
READMILL_CLIENT_ID = 'READMILL_CLIENT_ID'
READMILL_CLIENT_SECRET = 'READMILL_CLIENT_SECRET'
READMILL_API_ROOT = 'https://api.readmill.com/2'
READMILL_AUTH_URL = 'https://readmill.com/oauth/authorize'
READMILL_ACCESS_TOKEN_URL = 'https://readmill.com/oauth/token'

try:
  from local_settings import *
except ImportError:
  pass
