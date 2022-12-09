from flask import render_template, url_for
from nba_elo_system import app

@app.route('/')
def index():
    return render_template('index.html')
