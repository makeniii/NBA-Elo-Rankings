from flask import render_template, url_for
from nba_elo_system import app, db
from nba_elo_system.models import Season, Game, PlaysIn, Team


@app.route('/')
def index():
    teams = Team.query.order_by(Team.elo.desc()).all()
    return render_template('index.html', teams=teams)
