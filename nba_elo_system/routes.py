from flask import render_template, url_for
from nba_elo_system import app, db
from nba_elo_system.models import Season, Game, PlaysIn, Team
from nba_elo_system.elo_calculator import EloCalculator
import datetime
import pprint


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
    # get games from the following week
    # only tick over to next day after 6pm AEST
    start_date = (datetime.datetime.today() + datetime.timedelta(hours=6)).date()
    dates = [start_date] + [start_date + datetime.timedelta(days=i) for i in range(1, 7)]
    upcoming_week_schedule_data = PlaysIn.query.filter(PlaysIn.game_date.in_(dates)).order_by(PlaysIn.game_date.asc(), PlaysIn.game_id.asc(), PlaysIn.location.desc()).all()
    upcoming_week_schedule_data = [{'home': {'playsin': upcoming_week_schedule_data[i]}, 'away': {'playsin': upcoming_week_schedule_data[i+1]}} for i in range(0, len(upcoming_week_schedule_data), 2)]

    mon_games = list()
    tue_games = list()
    wed_games = list()
    thu_games = list()
    fri_games = list()
    sat_games = list()
    sun_games = list()

    for game in upcoming_week_schedule_data:
        game['home']['team'] = Team.query.filter(Team.id == game['home']['playsin'].team_id).one()
        game['away']['team'] = Team.query.filter(Team.id == game['away']['playsin'].team_id).one()
        game_day = game['home']['playsin'].game_date.strftime('%A')
        game['home'] = game['home']['team']
        game['away'] = game['away']['team']
        
        if game_day == 'Monday':
            mon_games.append(game)
        elif game_day == 'Tuesday':
            tue_games.append(game)
        elif game_day == 'Wednesday':
            wed_games.append(game)
        elif game_day == 'Thursday':
            thu_games.append(game)
        elif game_day == 'Friday':
            fri_games.append(game)
        elif game_day == 'Saturday':
            sat_games.append(game)
        elif game_day == 'Sunday':
            sun_games.append(game)
    
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

    for i in range(7):
        week_schedule[dates[i].weekday()]['date'] = dates[i]

    week_schedule.sort(key=lambda x: x['date'])

    return render_template(
        'schedule.html', 
        week_schedule=week_schedule, 
        round=round, 
        win_expectancy=EloCalculator.win_expectancy,
        projected_point_diff=EloCalculator.projected_point_diff,
        score_round=lambda x: x if x % 1 == 0.5 else round(x)
        )
