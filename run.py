from nba_elo_system import app
from nba_elo_system.db import update_db
from os import path
from pathlib import Path

if __name__ == '__main__':
    dbpath = Path(__file__).parent / 'nba_elo_system/nba.db'
    if path.isfile(dbpath):
        update_db(dbpath)
        app.run(debug=True)
    else:
        print('Please initialise DB before running server...', 'To initialise DB: run "nba_elo_system/db.py"')