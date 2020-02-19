from src.data import Holstep

steps = None
with Holstep() as db:
    steps = db.execute_many('SELECT DISTINCT Text FROM Step')

