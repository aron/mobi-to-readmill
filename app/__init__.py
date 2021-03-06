import os
import requests
from uuid import uuid4
from flask import Flask, request, session, flash, redirect, url_for, render_template

from settings import LOCAL_ROOT, READMILL_CLIENT_ID, READMILL_CLIENT_SECRET, READMILL_ACCESS_TOKEN_URL, READMILL_AUTH_URL, READMILL_API_ROOT, TMP_DIR
from tools.mobi_to_epub import mobi_to_epub

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if not os.path.isdir(TMP_DIR):
  os.makedirs(TMP_DIR)

def url_for_auth_callback():
  return '%s%s' % (LOCAL_ROOT, url_for('auth_callback'))

def redirect_to_readmill():
  callback_url = url_for_auth_callback()
  auth_url = '%s?response_type=code&client_id=%s&redirect_uri=%s' % (READMILL_AUTH_URL, READMILL_CLIENT_ID, callback_url)
  return redirect(auth_url)

def request_access_token(code):
  params = {
    'grant_type': 'authorization_code',
    'client_id': READMILL_CLIENT_ID,
    'client_secret': READMILL_CLIENT_SECRET,
    'redirect_uri': url_for_auth_callback(),
    'code': code
  }
  request = requests.post(READMILL_ACCESS_TOKEN_URL, params=params)

  return request.json()

def send_epub_to_readmill(filepath):
  url = '%s/me/library?client_id=%s' % (READMILL_API_ROOT, READMILL_CLIENT_ID)
  headers = {'Authorization': 'OAuth %s' % session['access_token']}
  files = {'library_item[asset]': open(filepath, 'rb')}

  response = requests.post(url, headers=headers, files=files)

  if response.status_code == 201:
    return response.json()
  elif response.status_code == 401:
    session.delete('access_token')
  else:
    app.logger.debug('Failed to send epub, server responded with: %s and body: %s' % (response.status_code, response.json()))

@app.route("/")
def home():
  if 'access_token' in session:
    return render_template('index.html')
  else:
    return render_template('login.html')

@app.route('/', methods=['POST'])
def upload():
  tmp_file = os.path.join(TMP_DIR, '%s.mobi' % uuid4())
  upload = request.files['file']
  upload.save(tmp_file)

  new_file = mobi_to_epub(tmp_file)
  result = send_epub_to_readmill(new_file)

  os.remove(tmp_file)
  os.remove(new_file)

  if request.is_xhr:
    if not result:
      return '', 500
    else:
      return '', 201
  else:
    return redirect(url_for('home'))

@app.route('/auth')
def auth():
  return redirect_to_readmill()

@app.route('/auth/callback')
def auth_callback():
  code = request.args.get('code')
  error = request.args.get('error')

  app.logger.debug('Callback with code: %s and error: %s' % (code, error))

  if error:
    flash('Sorry login errored with code: %s' % error)

  if code:
    json = request_access_token(code)
    app.logger.debug(json)

    if 'access_token' in json:
      flash('Yay, you logged in successfully')
      session['access_token'] = json.get('access_token')
    else:
      flash('Sorry, login failed with code: %s' % json['error'])

  return redirect(url_for('home'))
