from flask import Flask, request, render_template
app = Flask(__name__)

@app.route("/")
def home():
  return render_template('index.html')

@app.route('/', methods=['POST'])
def upload():
  f = request.files['mobi']
  f.save('/tmp/book.mobi')
  return redirect(url_for('home'))

if __name__ == "__main__":
  app.debug = True
  app.run()
