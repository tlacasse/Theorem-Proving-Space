import flask
import glob
from holstep import HolStep

db = HolStep()

app = flask.Flask('API')
app.config['DEBUG'] = True

@app.route('/')
def home():
    return flask.send_file('index.html')

@app.route('/content/style.css')
def content_style():
    return flask.send_file(glob.glob('web/_build/style*')[0])

@app.route('/content/script.js')
def content_script():
    return flask.send_file(glob.glob('web/_build/script*')[0])

@app.route('/favicon.ico')
def content_icon():
    return flask.send_file('web/favicon.ico')

@app.route('/api/holstep/conjecture/train/<i>', methods=['GET'])
def get_conjecture_train(i):
    return flask.jsonify(db.get_conjecture(int(i), train=True))

@app.route('/api/holstep/conjecture/test/<i>', methods=['GET'])
def get_conjecture_test(i):
    return flask.jsonify(db.get_conjecture(int(i), train=False))

app.run()
