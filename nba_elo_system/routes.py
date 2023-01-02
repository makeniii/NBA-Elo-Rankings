from flask import render_template, url_for
from nba_elo_system import app, db
from nba_elo_system.models import Season, Game, PlaysIn, Team


@app.route('/')
def index():
    teams = Team.query.order_by(Team.elo.desc()).all()
    game_change = list()
    short_change = list()
    long_change = list()

    for team in teams:
        game = None
        short = list()
        long = list()

        for plays_in in team.plays_in:
            if len(long) <= 27 and plays_in.outcome != None:
                if game == None and plays_in.outcome != None:
                    game = plays_in.elo_change

                if len(short) <= 9 and plays_in.outcome != None:
                    short.append(plays_in.elo_change)

                long.append(plays_in.elo_change)

        game_change.append(game)
        short_change.append(sum(short))
        long_change.append(sum(long))
        

    return render_template('index.html', teams=teams, game_change=game_change, short_change=short_change, long_change=long_change)
