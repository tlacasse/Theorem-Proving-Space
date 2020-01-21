import flask
import glob
from holstep import HolStep

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

@app.route('/api/holstep/conjecture/train/<int:i>', methods=['GET'])
def holstep_conjecture_train_get(i):
    with HolStep() as db:
        return flask.jsonify(db.get_conjecture(i, train=True))

@app.route('/api/holstep/conjecture/test/<int:i>', methods=['GET'])
def holstep_conjecture_test_get(i):
    with HolStep() as db:
        return flask.jsonify(db.get_conjecture(i, train=False))

app.run()
