from nba_elo_system import app, db_path
from nba_elo_system.db import update_db, initialise_db
from os import path
from pathlib import Path

if __name__ == '__main__':
    if not path.isfile(db_path):
        print(' * Please wait while initialising the server...')
        initialise_db(db_path)
    
    app.run(debug=True)