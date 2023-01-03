from flask import render_template, url_for
from nba_elo_system import app, db
from nba_elo_system.models import Season, Game, PlaysIn, Team
import datetime


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

@app.route('/schedule')
def schedule():
    # get next day games only after 6pm AEST
    start_date = (datetime.datetime.today() + datetime.timedelta(hours=6)).date()
    dates = [start_date] + [start_date + datetime.timedelta(days=i) for i in range(1, 7)]
    upcoming_week_schedule = PlaysIn.query.filter(PlaysIn.game_date.in_(dates)).order_by(PlaysIn.game_date.asc(), PlaysIn.game_id.asc(), PlaysIn.location.desc()).all()
    upcoming_week_schedule = [{'home': {'playsin': upcoming_week_schedule[i]}, 'away': {'playsin': upcoming_week_schedule[i+1]}} for i in range(0, len(upcoming_week_schedule), 2)]

    for game in upcoming_week_schedule:
        game['home']['team'] = Team.query.filter(Team.id == game['home']['playsin'].team_id).one()
        game['away']['team'] = Team.query.filter(Team.id == game['away']['playsin'].team_id).one()
    
    print(upcoming_week_schedule, len(upcoming_week_schedule))

    return render_template('schedule.html', schedule=upcoming_week_schedule)
