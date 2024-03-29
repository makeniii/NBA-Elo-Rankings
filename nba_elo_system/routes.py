from flask import render_template, url_for
from nba_elo_system import app, db, db_path
from nba_elo_system.models import Season, Game, PlaysIn, Team
from nba_elo_system.elo_calculator import EloCalculator
from nba_elo_system.utils import add_game_to_day
from nba_elo_system.db import update_db
import datetime
import pprint


@app.route('/')
def index():
    update_db(db_path)
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
    update_db(db_path)
    # get games from the following week
    start_date = datetime.datetime.today().date()
    dates = [start_date] + [start_date + datetime.timedelta(days=i) for i in range(1, 7)]
    game_data = Game.query.filter(Game.date.in_(dates), Game.status != 3).order_by(Game.date.asc(), Game.id.asc()).all()
    upcoming_week_schedule_data = [
            {
                'date': game_data[i].date, 
                'home': {'playsin': game_data[i].plays_in[1]},
                'away': {'playsin': game_data[i].plays_in[0]}
            } for i in range(0, len(game_data))
        ]

    mon_games = list()
    tue_games = list()
    wed_games = list()
    thu_games = list()
    fri_games = list()
    sat_games = list()
    sun_games = list()

    week_schedule = [
        {
            'day': 'Monday',
            'games': mon_games
        },
        {
            'day': 'Tuesday',
            'games': tue_games
        },
        {
            'day': 'Wednesday',
            'games': wed_games
        },
        {
            'day': 'Thursday',
            'games': thu_games
        },
        {
            'day': 'Friday',
            'games': fri_games
        },
        {
            'day': 'Saturday',
            'games': sat_games
        },
        {
            'day': 'Sunday',
            'games': sun_games
        }
    ]

    for game in upcoming_week_schedule_data:
        game['home']['team'] = Team.query.filter(Team.id == game['home']['playsin'].team_id).one()
        game['away']['team'] = Team.query.filter(Team.id == game['away']['playsin'].team_id).one()
        game_day = game['date'].strftime('%A')
        game['home'] = game['home']['team']
        game['away'] = game['away']['team']
        week_schedule = add_game_to_day(game, game_day, week_schedule)

    for i in range(7):
        week_schedule[dates[i].weekday()]['date'] = dates[i]

    week_schedule.sort(key=lambda x: x['date'])

    for day in week_schedule:
        if not day['games']:
            week_schedule.remove(day)

    return render_template(
        'schedule.html', 
        week_schedule=week_schedule, 
        round=round, 
        win_expectancy=EloCalculator.win_expectancy,
        projected_point_diff=EloCalculator.projected_point_diff,
        score_round=lambda x: x if x % 1 == 0.5 else round(x)
        )
