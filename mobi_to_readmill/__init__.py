from flask import Flask, request, session, flash, redirect, url_for, render_template
import requests

from mobi_to_readmill.mobi.mobi_to_epub import mobi_to_epub

LOCAL_ROOT = 'http://localhost:5000'
READMILL_CLIENT_ID = '26aec147008ebfd0a747605bb2db21bd'
READMILL_CLIENT_SECRET = 'b4e8ad628ce568f540d8976bc5f042d2'

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def url_for_auth_callback():
  return '%s%s' % (LOCAL_ROOT, url_for('auth_callback'))

def redirect_to_readmill():
  callback_url = url_for_auth_callback()
  auth_url = 'https://readmill.com/oauth/authorize?response_type=code&client_id=%s&redirect_uri=%s' % (READMILL_CLIENT_ID, callback_url)
  return redirect(auth_url)

def request_access_token(code):
  params = {
    'grant_type': 'authorization_code',
    'client_id': READMILL_CLIENT_ID,
    'client_secret': READMILL_CLIENT_SECRET,
    'redirect_uri': url_for_auth_callback(),
    'code': code
  }
  request = requests.post('https://readmill.com/oauth/token', params=params)

  return request.json()

def send_epub_to_readmill(filepath):
  url = 'https://api.readmill.com/v2/me/library?client_id=%s' % READMILL_CLIENT_ID
  headers = {'Authorization': 'OAuth %s' % session['access_token']}
  files = {'library_item[asset]': open(filepath, 'rb')}

  response = requests.post(url, headers=headers, files=files)

  if response.status_code == 201:
    return response.json()
  elif response.status_code == 401:
    session.delete('access_token')

@app.route("/")
def home():
  if 'access_token' in session:
    return render_template('index.html')
  else:
    return render_template('login.html')

@app.route('/', methods=['POST'])
def upload():
  f = request.files['file']
  f.save('/tmp/book.mobi')

  new_file = mobi_to_epub('/tmp/book.mobi')
  result = send_epub_to_readmill(new_file)

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

if __name__ == "__main__":
  app.debug = True
  app.run()
