import flask
import glob

from data import Holstep, Mizar, PageResults, HolstepParser, MizarParser

app = flask.Flask('API')
app.config['DEBUG'] = True
# this prevents spaces in json being removed somehow
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

class _STATE:
    
    def __init__(self):
        self.holstep_pages = PageResults(19)
        self.mizar_pages = PageResults(19)

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
    query = Holstep.build_search_conjecture(query, sort_by)
    with Holstep() as db:
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
    with Holstep() as db:
        conj = list(db.get_conjecture(i))
        # 3 == text
        conj[3] = HolstepParser().prettyprint(conj[3])
        return flask.jsonify(conj)
    
### Mizar
        
@app.route('/api/mizar/search/q/<string:query>', methods=['GET'])
def mizar_search(query):
    query = Mizar.build_search_theorem(query)
    with Mizar() as db:
        results = db.execute_many(query)
        STATE.mizar_pages.update_search(results)
        return mizar_search_page(0)
    
@app.route('/api/mizar/search/all', methods=['GET'])
def mizar_search_all():
    return mizar_search('')
    
@app.route('/api/mizar/search/page/<int:page>', methods=['GET'])
def mizar_search_page(page):
    return flask.jsonify(STATE.mizar_pages.fetch_page(page))

@app.route('/api/mizar/search/info', methods=['GET'])
def mizar_search_info():
    return flask.jsonify([len(STATE.mizar_pages.results), STATE.mizar_pages.pages])

@app.route('/api/mizar/theorem/<int:i>', methods=['GET'])
def mizar_theorem_get(i):
    with Mizar() as db:
        theorem, proof = db.get_theorem_and_proof(i)
        proof = MizarParser().parse(proof)
        return flask.jsonify([theorem, proof])
    
app.run()
