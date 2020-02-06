import flask
import glob

from data import HolStep, MLL, PageResults

app = flask.Flask('API')
app.config['DEBUG'] = True

class _STATE:
    
    def __init__(self):
        self.holstep_pages = PageResults(19)
        self.mll_pages = PageResults(19)

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
    
### HOLSTEP

@app.route('/api/holstep/search/q/<string:query>', methods=['GET'])
def holstep_search(query):
    sort_by = flask.request.args.get('sort')
    query = HolStep.build_search_conjecture(query, sort_by)
    with HolStep() as db:
        results = db.execute_many(query)
        STATE.holstep_pages.update_search(results)
        return holstep_search_page(0)
    
@app.route('/api/holstep/search/all', methods=['GET'])
def holstep_search_all():
    return holstep_search('')
    
@app.route('/api/holstep/search/page/<int:page>', methods=['GET'])
def holstep_search_page(page):
    return flask.jsonify(STATE.holstep_pages.fetch_page(page))

@app.route('/api/holstep/search/info', methods=['GET'])
def holstep_search_info():
    return flask.jsonify([len(STATE.holstep_pages.results), STATE.holstep_pages.pages])

@app.route('/api/holstep/conjecture/<int:i>', methods=['GET'])
def holstep_conjecture_get(i):
    with HolStep() as db:
        return flask.jsonify(db.execute_single('SELECT * FROM Conjecture WHERE Id={}'.format(i)))
    
### MLL
        
@app.route('/api/mll/search/q/<string:query>', methods=['GET'])
def mll_search(query):
    query = MLL.build_search_conjecture(query)
    with MLL() as db:
        results = db.execute_many(query)
        STATE.mll_pages.update_search(results)
        return mll_search_page(0)
    
@app.route('/api/mll/search/all', methods=['GET'])
def mll_search_all():
    return mll_search('')
    
@app.route('/api/mll/search/page/<int:page>', methods=['GET'])
def mll_search_page(page):
    return flask.jsonify(STATE.mll_pages.fetch_page(page))

@app.route('/api/mll/search/info', methods=['GET'])
def mll_search_info():
    return flask.jsonify([len(STATE.mll_pages.results), STATE.mll_pages.pages])
    
app.run()
