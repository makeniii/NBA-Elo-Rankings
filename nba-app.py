from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.static import teams
from nba_api.live.nba.endpoints import boxscore
from nba_api.stats.endpoints import leaguegamelog
import pandas as pd
import numpy as np
import math

class Game():
    home_team = ''
    away_team = ''
    score = {'home': -1, 'away': -1}        # {'home': PTS, 'away': PTS}
    date = ''                               # yyyy-mm-dd

    def __init__(self, id, home_team, home_pts, away_team, away_pts, date):
        self.id = id
        self.set_home_team(home_team)
        self.set_away_team(away_team)
        self.set_score(home_pts, away_pts)
        self.set_date(date)

    def __str__(self) -> str:
        return 'id: ' + str(self.id) + ', home_team: ' + self.home_team + ', away_team: ' + self.away_team + ', score: ' + str(self.score) + ', ' + self.date

    def set_score(self, home, away):
        self.score['home'] = home
        self.score['away'] = away
    
    def set_date(self, date):
        self.date = date
    
    def set_home_team(self, home_team):
        self.home_team = home_team
    
    def set_away_team(self, away_team):
        self.away_team = away_team

    def point_diff(self) -> int:
        return abs(self.score['home'] - self.score['away'])


regular_season_games = leaguegamelog.LeagueGameLog(season='2021-22').get_data_frames()[0]
playoff_games = leaguegamelog.LeagueGameLog(season='2021-22', season_type_all_star='Playoffs').get_data_frames()[0]

sorted_regular_season_games = regular_season_games.sort_values(by=['GAME_ID'])
sorted_regular_season_games = sorted_regular_season_games.drop(index=sorted_regular_season_games.index[::2]).reset_index(drop=True).get(['GAME_DATE', 'TEAM_NAME', 'MATCHUP', 'PTS', 'PLUS_MINUS', 'GAME_ID'])
sorted_playoff_games = playoff_games.sort_values(by=['GAME_ID'])
sorted_playoff_games = sorted_playoff_games.drop(index=sorted_playoff_games.index[::2]).reset_index(drop=True).get(['GAME_DATE', 'TEAM_NAME', 'MATCHUP', 'PTS', 'PLUS_MINUS', 'GAME_ID'])

print(sorted_regular_season_games)
print(sorted_playoff_games)

frames = [sorted_regular_season_games, sorted_playoff_games]

all_games = pd.concat(frames).reset_index(drop=True)

print(all_games)

games = []

for game in all_games.to_dict('records'):
    matchup = game['MATCHUP'].split(' vs. ')

    if len(matchup) == 1:
        away_team = game['MATCHUP'].split(' @ ')[0]
        home_team = game['MATCHUP'].split(' @ ')[1]
        away_pts = game['PTS']
        home_pts = away_pts - game['PLUS_MINUS']
    else:
        away_team = matchup[1]
        home_team = matchup[0]
        home_pts = game['PTS']
        away_pts = home_pts - game['PLUS_MINUS']

    x = Game(game['GAME_ID'], home_team, home_pts, away_team, away_pts, game['GAME_DATE'])

    games.append(x)

    print(x)
