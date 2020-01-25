import flask
import glob
import math

import holstep
from holstep import HolStep

app = flask.Flask('API')
app.config['DEBUG'] = True

class _STATE:
    
    def __init__(self):
        self.holstep_search_results = []
        self.holstep_search_pages = 1
        self.HOLSTEP_SEARCH_PERPAGE = 19
        
    def update_holstep_search(self, results):
        self.holstep_search_results = results
        self.holstep_search_pages = math.ceil(len(results) / self.HOLSTEP_SEARCH_PERPAGE)
        
    def fetch_holstep_search_page(self, page):
        size = self.HOLSTEP_SEARCH_PERPAGE
        return self.holstep_search_results[size * page : size * (page + 1)]

STATE = _STATE()

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
    
@app.route('/api/holstep/search/q/<string:query>', methods=['GET'])
def holstep_search(query):
    query = holstep.build_search_conjecture(query)
    with HolStep() as db:
        results = db.execute_many(query)
        STATE.update_holstep_search(results)
        return holstep_search_page(0)
    
@app.route('/api/holstep/search/all', methods=['GET'])
def holstep_search_all():
    return holstep_search('')
    
@app.route('/api/holstep/search/page/<int:page>', methods=['GET'])
def holstep_search_page(page):
    return flask.jsonify(STATE.fetch_holstep_search_page(page))

@app.route('/api/holstep/search/info', methods=['GET'])
def holstep_search_info():
    return flask.jsonify([len(STATE.holstep_search_results), STATE.holstep_search_pages])

@app.route('/api/holstep/conjecture/<int:i>', methods=['GET'])
def holstep_conjecture_get(i):
    with HolStep() as db:
        return flask.jsonify(db.execute_single('SELECT * FROM Conjecture WHERE Id={}'.format(i)))
    
app.run()
