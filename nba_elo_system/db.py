import requests
import pprint
import json
import pandas as pd
import progressbar
import sqlite3
from sqlite3 import OperationalError
from pathlib import Path
import datetime

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
            'Year': int(year),
            'Name': year_name
        }]
    )

    children = standings_json['children']

    playoff_teams = list()
    playin_teams = list()

    playoff_clinched = 1
    playin_clinched = 6
    playin_won = 7
    eliminated = 4

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

    # print()
    # for children in standings_json['children']:
    #     for team in children['standings']['entries']:
    #         print(team['stats'][8]['displayValue'] + '. ' + team['team']['displayName'])
    #     print()

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
    game_table = pd.DataFrame(columns=['ID', 'SeasonID', 'Type', 'Status'])

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

            if game_id in game_table['ID'].values:
                continue
            
            game_entry = pd.DataFrame(
                [{
                    'ID': game_id,
                    'SeasonID': season_year,
                    'Type': season_type,
                    'Status': int(game_status)
                }]
            )

            game_table = pd.concat([game_table, game_entry])

            if game_status == '3':
                home = pd.DataFrame(
                    [{
                        'GameID': game_id,
                        'TeamID': int(game['competitors'][0]['id']),
                        'Score': int(game['competitors'][0]['score']['value']),
                        'Location': game['competitors'][0]['homeAway'],
                        'Outcome': 'W' if game['competitors'][0]['winner'] else 'L'
                    }]
                )

                away = pd.DataFrame(
                    [{
                        'GameID': game_id,
                        'TeamID': int(game['competitors'][1]['id']),
                        'Score': int(game['competitors'][1]['score']['value']),
                        'Location': game['competitors'][1]['homeAway'],
                        'Outcome': 'W' if game['competitors'][1]['winner'] else 'L'
                    }]
                )

                playsin_table = pd.concat([playsin_table, home, away])
            elif game_status == '1' or game_status == '2':
                home = pd.DataFrame(
                    [{
                        'GameID': game_id,
                        'TeamID': int(game['competitors'][0]['id']),
                        'Score': 0,
                        'Location': game['competitors'][0]['homeAway'],
                        'Outcome': None
                    }]
                )

                away = pd.DataFrame(
                    [{
                        'GameID': game_id,
                        'TeamID': int(game['competitors'][1]['id']),
                        'Score': 0,
                        'Location': game['competitors'][1]['homeAway'],
                        'Outcome': None
                    }]
                )

                playsin_table = pd.concat([playsin_table, home, away])
            else:
                print('game status: ' + game_status + '. What to do?')


    # print(season_table)
    # print()
    # print(team_table)
    # print()
    # print(game_table)
    # print()
    # print(playsin_table)

    dbpath = Path(__file__).parent / 'nba.db'
    con = sqlite3.connect(dbpath)

    season_table.to_sql(name='Season', con=con, if_exists='append', index=False)
    game_table.to_sql(name='Game', con=con, if_exists='append', index=False)
    playsin_table.to_sql(name='PlaysIn', con=con, if_exists='append', index=False)

    con.commit()
    con.close()

    # print()
    # print(year + ' SEASON COMPLETE - ' + str(len(playsin_table)) + ' GAMES COMPILIED')
    # print()
    return progress


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

widgets = [' [',
            progressbar.Timer(format= 'elapsed time: %(elapsed)s'),
            '] ',
            progressbar.Bar('*'),' (',
            progressbar.ETA(), ') ',
            ]
    
bar = progressbar.ProgressBar(maxval=32700*len(years), widgets=widgets).start()
prog = 0

dbpath = Path(__file__).parent / 'nba.db'
con = sqlite3.connect(dbpath)
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
            'ID': int(team['team']['id']),
            'Name': team['team']['displayName'],
            'ShortName': team['team']['shortDisplayName'],
            'Abbreviation': team['team']['abbreviation'],
            'Elo': 1500
        }]
    )])

team_table.to_sql(name='Team', con=con, if_exists='append', index=False)

con.commit()
con.close()

for year in years:
    prog = create_nba_season_data(year, teams, prog, bar)