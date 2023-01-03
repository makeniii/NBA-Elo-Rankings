import requests
import pprint
import json
import pandas as pd
import progressbar
import sqlite3
from sqlite3 import OperationalError
from pathlib import Path
import datetime
import os


if __name__ == '__main__':
    from elo_calculator import EloCalculator
    
else:
    from nba_elo_system.elo_calculator import EloCalculator


FORCE_INIT = True


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_team(teams, team_key):
    for x in teams:
        if team_key == x['abbreviation']:
            return x


def executeScriptsFromFile(filename, cur):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            cur.execute(command)
        except OperationalError as msg:
            print("Command skipped: ", msg)


'''
Game        = schedule_json['events']['competitions'][0] - seems like index is always 1. At least for nba games.
HomeTeam    = Game['competitors'][0]
AwayTeam    = Game['competitors'][1]
Game ID     = Game['id']
Game status = Game['status']['type']['id'] - only accept 1/3

Game status - all strings
1 = scheduled
2 = live
3 = completed
6 = postponed
4/5 = ?
22 = end of third quarter

HomeTeam/AwayTeam Location  = Game['competitors'][0/1]['homeAway']
HomeTeam/AwayTeam Outcome   = Game['competitors'][0/1]['winner']
HomeTeam/AwayTeam Score     = Game['competitors'][0/1]['score']['value'] - floating value returned


Season      = schedule_json['requestedSeason']
Name        = Season['displayName']
Year        = Season['year']

* notes

When getting the schedule of a team. That team will have an additional 'leaders' key in HomeTeam/AwayTeam. 'leaders' will contain
the leaders of that team's points, rebounds, and assists.

https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/{team_abbreviation}/schedule - gets most recent sesaon
https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/{team_abbreviation}/schedule?season={season} - gets requested season
https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/{team_abbreviation}/schedule?seasontype={seasontype} - most recent requested season type

seasontype
1 = pre season
2 = regular season
3 = post season
5 = play ins

schedule_json['season'] is info on current season.


standings['entries']['stats'] - has streak wins !!
'''

def create_nba_season_data(year, teams, progress, bar):
    dbpath = Path(__file__).parent / 'nba.db'
    con = sqlite3.connect(dbpath)
    cur = con.cursor()

    cur.execute(
        '''UPDATE team SET elo = ROUND(elo * 0.75 + (:carry_over))''', 
        {'carry_over': 0.25 * EloCalculator.elo_avg}
    )

    regular_season = '2'
    post_season = '3'
    play_ins = '5'

    year_name = list(year)

    if year_name[3] == '0':
        if year_name[2] == '0':
            if year_name[1] == '0':
                year_name[0] = str(int(year_name[0]) - 1)
                year_name[1] = '9'
            
            year_name[1] = str(int(year_name[1]) - 1)
            year_name[2] = '9'
        year_name[2] = str(int(year_name[2]) - 1)
        year_name[3] = '9'
    else:
        year_name[3] = str(int(year_name[3]) - 1)

    year_name = ''.join(year_name)
    year_name = year_name + '-' + year[2:]

    seasontype = regular_season
    standings_json = requests.get('https://site.api.espn.com/apis/v2/sports/basketball/nba/standings?season=' + year + '&sort=playoffseed').json()
    season_table = pd.DataFrame(
        [{
            'year': int(year),
            'name': year_name
        }]
    )

    children = standings_json['children']

    playoff_teams = list()
    playin_teams = list()

    playoff_clinched = 1
    playin_clinched = 6
    playin_won = 7

    for children in standings_json['children']:
        for i in range(6):
            playoff_teams.append(children['standings']['entries'][i]['team']['id'])

        if int(year) > 2020:
            for i in range(6, 10):
                if children['standings']['entries'][i]['stats'][2]['value'] == playoff_clinched:
                    playoff_teams.append(children['standings']['entries'][i]['team']['id'])
                elif children['standings']['entries'][i]['stats'][2]['value'] == playin_clinched:
                    playin_teams.append(children['standings']['entries'][i]['team']['id'])
                elif children['standings']['entries'][i]['stats'][2]['value'] == playin_won:
                    playoff_teams.append(children['standings']['entries'][i]['team']['id'])
                    playin_teams.append(children['standings']['entries'][i]['team']['id'])
        else:
            for i in range(6, 8):
                playoff_teams.append(children['standings']['entries'][i]['team']['id'])

    schedule_json = json.loads('[]')
    index = -1

    for i in range(len(standings_json['seasons'])):
        if standings_json['seasons'][i]['year'] == int(year):
            index = i
            break

    if index == -1:
        raise Exception('Year: ' + year + ' does not exist')

    curr_date = datetime.date.today()
    playoff_start_date = datetime.datetime.strptime(standings_json['seasons'][index]['types'][2]['startDate'][:10], '%Y-%m-%d').date()

    if int(year) >= 2020:
        playin_start_date = datetime.datetime.strptime(standings_json['seasons'][index]['types'][4]['startDate'][:10], '%Y-%m-%d').date()

    for team in teams:
        seasontype = regular_season
        regular_season_json = requests.get('https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/' + team['id'] + '/schedule?season=' + year + '&seasontype=' + seasontype).json()
        schedule_json.append(regular_season_json)


        if int(year) >= 2020 and curr_date > playin_start_date:
            if team['id'] in playin_teams:
                seasontype = play_ins
                playin_json = requests.get('https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/' + team['id'] + '/schedule?season=' + year + '&seasontype=' + seasontype).json()
                if 'requestedSeason' not in playin_json:
                    print(playin_json['team']['displayName'] + ': No play ins')
                else:
                    schedule_json.append(playin_json)

        if curr_date > playoff_start_date:
            if team['id'] in playoff_teams:
                seasontype = post_season
                post_season_json = requests.get('https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/' + team['id'] + '/schedule?season=' + year + '&seasontype=' + seasontype).json()
                if 'requestedSeason' not in post_season_json:
                    print(post_season_json['team']['displayName'] + ': No playoffs')
                else:
                    schedule_json.append(post_season_json)
        
        bar.update(progress)
        progress += 1000

    playsin_table = pd.DataFrame()
    game_table = pd.DataFrame(columns=['id', 'season_id', 'type', 'status'])

    for season in schedule_json:
        season_type = season['requestedSeason']['name']
        season_year = int(season['requestedSeason']['year'])

        for event in season['events']:
            progress += 1
            bar.update(progress)
            game = event['competitions'][0]
            game_status = game['status']['type']['id']

            if game_status in ['6', '4', '5']:
                continue
            
            game_id = int(game['id'])

            if game_id in game_table['id'].values:
                continue

            game_entry = pd.DataFrame(
                [{
                    'id': game_id,
                    'season_id': season_year,
                    'type': season_type,
                    'status': int(game_status),
                    'date': game['date'][:-7],
                    'is_calculation_required': 1
                }]
            )

            game_table = pd.concat([game_table, game_entry])

            if game_status == '3':
                home = pd.Series(
                    {
                        'game_id': game_id,
                        'team_id': int(game['competitors'][0]['id']),
                        'score': int(game['competitors'][0]['score']['value']),
                        'location': 'home',
                        'outcome': 'W' if game['competitors'][0]['winner'] else 'L',
                        'elo_change': None
                    }
                )

                away = pd.Series(
                    {
                        'game_id': game_id,
                        'team_id': int(game['competitors'][1]['id']),
                        'score': int(game['competitors'][1]['score']['value']),
                        'location': 'away',
                        'outcome': 'W' if game['competitors'][1]['winner'] else 'L',
                        'elo_change': None
                    }
                )

            else:
                home = pd.Series(
                    {
                        'game_id': game_id,
                        'team_id': int(game['competitors'][0]['id']),
                        'score': 0,
                        'location': 'home',
                        'outcome': None,
                        'elo_change': None
                    }
                )

                away = pd.Series(
                    {
                        'game_id': game_id,
                        'team_id': int(game['competitors'][1]['id']),
                        'score': 0,
                        'location': 'away',
                        'outcome': None,
                        'elo_change': None
                    }
                )

            playsin_table = pd.concat([playsin_table, pd.DataFrame([home, away])])

    season_table.to_sql(name='season', con=con, if_exists='append', index=False)
    game_table.to_sql(name='game', con=con, if_exists='append', index=False)
    playsin_table.to_sql(name='plays_in', con=con, if_exists='append', index=False)

    con.commit()
    con.close()

    return progress

def initialise_db(dbpath):
    years = [
        '2005',
        '2006',
        '2007',
        '2008',
        '2009',
        '2010',
        '2011',
        '2012',
        '2013',
        '2014',
        '2015',
        '2016',
        '2017',
        '2018',
        '2019',
        '2020',
        '2021',
        '2022',
        '2023'
        ]

    # years = [
    #     '2023'
    # ]

    widgets = [' [',
                progressbar.Timer(format= 'elapsed time: %(elapsed)s'),
                '] ',
                progressbar.Bar('*'),' (',
                progressbar.ETA(), ') ',
                ]
        
    bar = progressbar.ProgressBar(maxval=32700*len(years), widgets=widgets).start()
    prog = 0

    con = sqlite3.connect(dbpath)
    con.row_factory = dict_factory
    cur = con.cursor()

    filepath = Path(__file__).parent / 'schema.sql'
    executeScriptsFromFile(filepath, cur)

    data = requests.get('https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams?limit=30').json()

    teams = list()
    team_table = pd.DataFrame()

    for team in data['sports'][0]['leagues'][0]['teams']:
        teams.append(team['team'])
        
        team_table = pd.concat([team_table, pd.DataFrame(
            [{
                'id': int(team['team']['id']),
                'name': team['team']['displayName'],
                'short_name': team['team']['shortDisplayName'],
                'abbreviation': team['team']['abbreviation'],
                'elo': 1500
            }]
        )])

    team_table.to_sql(name='team', con=con, if_exists='append', index=False)

    standings = requests.get('https://site.api.espn.com/apis/v2/sports/basketball/nba/standings?season=2023').json()

    for conf in standings['children']:
        for team in conf['standings']['entries']:
            team_id = team['team']['id']
            win, loss = team['stats'][11]['displayValue'].split('-')
            games_played = int(win) + int(loss)
            cur.execute('''UPDATE team SET games_played = (?) WHERE id = (?)''', (games_played, team_id,))

    con.commit()

    for year in years:
        prog = create_nba_season_data(year, teams, prog, bar)

    cur.execute('''SELECT * FROM season''')
    seasons = cur.fetchall()

    for season in seasons:
        cur.execute('''
        SELECT plays_in.game_id, plays_in.team_id, plays_in.score, plays_in.location, plays_in.outcome
        FROM plays_in
        INNER JOIN game ON plays_in.game_id = game.id
        WHERE game.season_id = (?)
        AND plays_in.outcome IS NOT NULL
        ORDER BY game.date ASC
        ''', (season['year'],))

        playsin_df = cur.fetchall()
        cur.execute('''SELECT * FROM team''')
        team_df = pd.DataFrame(cur.fetchall(), columns=['id', 'name', 'short_name', 'abbreviation', 'elo', 'games_played'])
        team_df['elo'] = round(team_df['elo'] * 0.75 + 1500 * 0.25)
        team_df = team_df.astype({"elo": int})

        season_length = len(playsin_df)
        
        for i in range(0, season_length, 2):
            team_a = team_df[team_df['id'] == playsin_df[i]['team_id']]
            team_b = team_df[team_df['id'] == playsin_df[i+1]['team_id']]
            team_a_elo = team_a.iloc[0]['elo']
            team_b_elo = team_b.iloc[0]['elo']

            if playsin_df[i]['outcome'] == 'W':
                winner = 0
                RDiff = team_a_elo - team_b_elo
                margin = playsin_df[i]['score'] - playsin_df[i+1]['score']
            else:
                winner = 1
                RDiff = team_b_elo - team_a_elo
                margin = playsin_df[i+1]['score'] - playsin_df[i]['score']

            mov = EloCalculator.margin_of_victory(
                    margin,
                    RDiff,
                    playsin_df[i+winner]['location']
                )
            
            team_a_elo_change = EloCalculator.elo_change(team_a_elo, playsin_df[i]['outcome'], team_b_elo, playsin_df[i]['location'], mov)

            team_df.loc[team_df['id'] == playsin_df[i]['team_id'], 'elo'] = team_a_elo + team_a_elo_change
            team_df.loc[team_df['id'] == playsin_df[i+1]['team_id'], 'elo'] = team_b_elo - team_a_elo_change
            cur.execute('''UPDATE game SET is_calculation_required = 0 WHERE id = (?)''', (playsin_df[i]['game_id'],))
            cur.execute('''UPDATE plays_in SET elo_change = (?) WHERE game_id = (?) AND team_id = (?)''', (team_a_elo_change, playsin_df[i]['game_id'], playsin_df[i]['team_id'],))
            cur.execute('''UPDATE plays_in SET elo_change = (?) WHERE game_id = (?) AND team_id = (?)''', (-team_a_elo_change, playsin_df[i+1]['game_id'], playsin_df[i+1]['team_id'],))

        team_df.to_sql(name='team', con=con, if_exists='replace', index=False)

    con.close()


def get_updated_games(start_date, end_date):
    game_table = list()
    playsin_table = list()
    start_date = str(start_date).replace('-','')
    end_date = str(end_date).replace('-','')
    data = requests.get(
        'http://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?&dates='
        + start_date
        + '-' 
        + end_date
    ).json()

    for event in data['events']:
        game = event['competitions'][0]
        game_status = game['status']['type']['id']
        
        game_id = int(game['id'])

        game_entry = {
            'id': game_id,
            'status': int(game_status)
        }

        game_table.append(game_entry)

        if game_status == '3':
            home = {
                'game_id': game_id,
                'team_id': int(game['competitors'][0]['id']),
                'score': int(game['competitors'][0]['score']),
                'outcome': 'W' if game['competitors'][0]['winner'] else 'L'
            }

            away = {
                    'game_id': game_id,
                    'team_id': int(game['competitors'][1]['id']),
                    'score': int(game['competitors'][1]['score']),
                    'outcome': 'W' if game['competitors'][1]['winner'] else 'L'
            }

            playsin_table.append(home)
            playsin_table.append(away)
    
    return [game_table, playsin_table]


def update_db(dbpath):
    con = sqlite3.connect(dbpath)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute('''SELECT date FROM game WHERE status = 3 ORDER BY date DESC''')

    # current date
    end_date = (datetime.datetime.today() - datetime.timedelta(days=1, hours=16)).date()

    # date of last game played in database
    start_date = cur.fetchone()['date']
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date() - datetime.timedelta(days=1)

    if end_date > start_date:
        print(' * Updating DB ...')
        game_table, playsin_table = get_updated_games(start_date, end_date)

        for game in game_table:
            cur.execute('''
            UPDATE game
            SET status = (?)
            WHERE id = (?)
            ''', (game['status'], game['id'],))
        
        for plays_in in playsin_table:
            cur.execute('''
            UPDATE plays_in
            SET score = (?), outcome = (?)
            WHERE game_id = (?) AND team_id = (?)
            ''', (plays_in['score'], plays_in['outcome'], plays_in['game_id'], plays_in['team_id'],))

        cur.execute('''
        SELECT plays_in.team_id, COUNT(*) as games_played
        FROM plays_IN
        INNER JOIN game ON plays_in.game_id = game.id
        WHERE game.season_id = 2023
        AND game.status = 3
        GROUP BY plays_in.team_id
        ''')

        calculate_elos(cur, [dictionary['id'] for dictionary in game_table])
        print(' * ...Done!')

    con.commit()
    con.close()


def calculate_elos(cur, game_ids):
    for game_id in game_ids:
        cur.execute('''
        SELECT plays_in.game_id, plays_in.team_id, plays_in.score, plays_in.location, plays_in.outcome
        FROM plays_in
        INNER JOIN game ON plays_in.game_id = game.id
        WHERE game.id = (?)
        AND game.is_calculation_required = 1
        ORDER BY game.date ASC
        ''', (game_id,))
        
        plays_in = cur.fetchall()
        
        if len(plays_in) == 0:
            continue

        team_a, team_b = plays_in

        cur.execute('''SELECT elo FROM team WHERE id = (?)''', (team_a['team_id'],))
        team_a_elo = cur.fetchone()['elo']

        cur.execute('''SELECT elo FROM team WHERE id = (?)''', (team_b['team_id'],))
        team_b_elo = cur.fetchone()['elo']

        if team_a['outcome'] == 'W':
            RDiff = team_a_elo - team_b_elo
            margin = team_a['score'] - team_b['score']
            location = team_a['location']
        else:
            RDiff = team_b_elo - team_a_elo
            margin = team_b['score'] - team_a['score']
            location = team_b['location']

        mov = EloCalculator.margin_of_victory(
            margin,
            RDiff,
            location
        )

        team_a_elo_change = EloCalculator.elo_change(
            team_a_elo,
            team_a['outcome'],
            team_b_elo,
            team_a['location'],
            mov
        )

        team_a_elo = team_a_elo + team_a_elo_change
        team_b_elo = team_b_elo - team_a_elo_change
        cur.execute('''UPDATE team SET elo = (?) WHERE id = (?)''', (team_a_elo, team_a['team_id'],))
        cur.execute('''UPDATE team SET elo = (?) WHERE id = (?)''', (team_b_elo, team_b['team_id'],))
        cur.execute('''UPDATE game SET is_calculation_required = 0 WHERE id = (?)''', (game_id,))
        cur.execute('''UPDATE plays_in SET elo_change = (?) WHERE game_id = (?) AND team_id = (?)''', (team_a_elo_change, team_a['game_id'], team_a['team_id'],))
        cur.execute('''UPDATE plays_in SET elo_change = (?) WHERE game_id = (?) AND team_id = (?)''', (-team_a_elo_change, team_b['game_id'], team_b['team_id'],))
    

if __name__ == '__main__':
    dbpath = Path(__file__).parent / 'nba.db'
    if os.path.isfile(dbpath) and not FORCE_INIT:
        update_db(dbpath)
    else:
        initialise_db(dbpath)