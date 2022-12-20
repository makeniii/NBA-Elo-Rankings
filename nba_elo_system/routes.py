from flask import render_template, url_for
from nba_elo_system import app
from nba_elo_system.models import season_21


@app.route('/')
def index():
    ordered_list = season_21.teams
    ordered_list.sort(key=lambda x: x.elo.elo, reverse=True)
    return render_template('index.html', teams=ordered_list)
