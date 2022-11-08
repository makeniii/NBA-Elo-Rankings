from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.static import teams
from nba_api.live.nba.endpoints import boxscore
from nba_api.stats.endpoints import leaguegamelog
from nba_api.stats.endpoints import commonplayoffseries
import pandas as pd
import numpy as np
import datetime
import math
import time

'''
A few helper functions just to shorten the length of code to make it easier to read
'''
def get_games(season, type) -> pd.DataFrame:
    return leaguegamelog.LeagueGameLog(season=season, season_type_all_star=type).get_data_frames()[0]

def get_games_default(type) -> pd.DataFrame:
    return leaguegamelog.LeagueGameLog(season_type_all_star=type).get_data_frames()[0]

class Game():
    def __init__(self, id, home_team, home_pts, away_team, away_pts, date):
        self.id = id
        self.home_team = home_team
        self.away_team = away_team
        self.score = {'HOME': home_pts, 'AWAY': away_pts}
        self.date = date

    def __str__(self) -> str:
        return 'id: ' + str(self.id) + ', home_team: ' + self.home_team + ', away_team: ' + self.away_team + ', score: ' + str(self.score) + ', ' + self.date
    
    # do I need both?
    def __repr__(self) -> str:
        return 'id: ' + str(self.id) + ', home_team: ' + self.home_team + ', away_team: ' + self.away_team + ', score: ' + str(self.score) + ', ' + self.date

    def point_diff(self) -> int:
        return abs(self.score['HOME'] - self.score['HOME'])

class Schedule():
    def __init__(self) -> None:
        self.games = []
        pass

    def add_games(self, games):
        self.games.extend(games)
    
    def __str__(self) -> str:
        return str(self.games)

class TeamSchedule(Schedule):
    def __init__(self) -> None:
        super().__init__()

    def add_games(self, games):
        return super().add_games(games)

class PR():
    def __init__(self) -> None:
        self.x = 100
        self.home_adv = 0.1
        self.pr = -1

    def win_expectancy_calc(self, Ro, OPPRo, is_home) -> int:
        return 1 / (10**(-((Ro - OPPRo) + Ro*(is_home*self.home_adv)) / self.x) + 1)

class Team():
    def __init__(self, name) -> None:
        self.name = name
        self.pr = PR()
        self.schedule = TeamSchedule()

    def __repr__(self) -> str:
        return self.name
        
    def add_to_schedule(self, games):
        self.schedule.add_games(games)

    '''
    I set the team schedule which is a list of dictionaries that include:
        W: boolean
        PTS: int
        Point Diff: int
        Opponent: str
        Home: boolean
        Date: str
        Game: Game data - <Game>
    '''
    def create_schedule(self):
        regular_season_games_curr = get_games_default('Regular Season')
        time.sleep(1)
        regular_season_games_curr = regular_season_games_curr[regular_season_games_curr['TEAM_ABBREVIATION'] == self.name].reset_index(drop=True)
        playoff_games_curr = get_games_default('Playoffs')
        time.sleep(1)
        playoff_games_curr = playoff_games_curr[playoff_games_curr['TEAM_ABBREVIATION'] == self.name].reset_index(drop=True)

        # Note: Not sure why there is a 2 at the front but I cut it off anyways. Not sure if there is always a 2 before the year but it looks to be so.
        year = int(regular_season_games_curr.SEASON_ID[0][1:])

        regular_season_games_hist = get_games(year-1, 'Regular Season')
        time.sleep(1)
        regular_season_games_hist = regular_season_games_hist[regular_season_games_hist['TEAM_ABBREVIATION'] == self.name]
        playoff_games_hist = get_games(year-1, 'Playoffs')
        time.sleep(1)
        playoff_games_hist = playoff_games_hist[playoff_games_hist['TEAM_ABBREVIATION'] == self.name]

        # Remember to drop duplicates for the schedule for the season class
        sorted_regular_season_games_curr = regular_season_games_curr.sort_values(by=['GAME_ID'])
        sorted_regular_season_games_curr = sorted_regular_season_games_curr.reset_index(drop=True).get(['GAME_DATE', 'TEAM_NAME', 'MATCHUP', 'PTS', 'PLUS_MINUS', 'GAME_ID'])
        sorted_regular_season_games_hist = regular_season_games_hist.sort_values(by=['GAME_ID'])
        sorted_regular_season_games_hist = sorted_regular_season_games_hist.reset_index(drop=True).get(['GAME_DATE', 'TEAM_NAME', 'MATCHUP', 'PTS', 'PLUS_MINUS', 'GAME_ID'])
        sorted_playoff_games_hist = playoff_games_hist.sort_values(by=['GAME_ID'])
        sorted_playoff_games_hist = sorted_playoff_games_hist.reset_index(drop=True).get(['GAME_DATE', 'TEAM_NAME', 'MATCHUP', 'PTS', 'PLUS_MINUS', 'GAME_ID'])

        frames = []

        regular_season_type_curr = ['Regular Season']*len(sorted_regular_season_games_curr)
        sorted_regular_season_games_curr['TYPE'] = regular_season_type_curr

        regular_season_type_hist = ['Regular Season']*len(sorted_regular_season_games_hist)
        sorted_regular_season_games_hist['TYPE'] = regular_season_type_hist

        playoff_type_hist = ['Playoffs']*len(sorted_playoff_games_hist)
        sorted_playoff_games_hist['TYPE'] = playoff_type_hist

        if not playoff_games_curr.empty:
            sorted_playoff_games_curr = playoff_games_curr.sort_values(by=['GAME_ID'])
            sorted_playoff_games_curr = sorted_playoff_games_curr.reset_index(drop=True).get(['GAME_DATE', 'TEAM_NAME', 'MATCHUP', 'PTS', 'PLUS_MINUS', 'GAME_ID'])
            playoff_type_curr = ['Playoffs']*len(sorted_playoff_games_curr)
            sorted_playoff_games_curr['TYPE'] = playoff_type_curr

            frames = [sorted_regular_season_games_hist, sorted_playoff_games_hist, sorted_regular_season_games_curr, sorted_playoff_games_curr]
        else:
            frames = [sorted_regular_season_games_hist, sorted_playoff_games_hist, sorted_regular_season_games_curr]
        
        all_games = pd.concat(frames).reset_index(drop=True)

        games = []

        for game in all_games.to_dict('records'):
            x = {}
            matchup = game['MATCHUP'].split(' vs. ')
            x['PTS'] = game['PTS']
            x['PLUS_MINUS'] =  game['PLUS_MINUS']
            x['DATE'] = game['GAME_DATE']

            if x['PLUS_MINUS'] > 0:
                x['W'] = True
            else:
                x['W'] = False

            if len(matchup) == 1:
                away_team = game['MATCHUP'].split(' @ ')[0]
                home_team = game['MATCHUP'].split(' @ ')[1]
                x['OPPONENT'] = home_team
                x['HOME'] = False
                away_pts = game['PTS']
                home_pts = away_pts - game['PLUS_MINUS']
            else:
                away_team = matchup[1]
                home_team = matchup[0]
                x['OPPONENT'] = away_team
                x['HOME'] = True
                home_pts = game['PTS']
                away_pts = home_pts - game['PLUS_MINUS']
            

            x['GAME'] = Game(game['GAME_ID'], home_team, home_pts, away_team, away_pts, game['GAME_DATE'], game['TYPE'])

            games.append(x)

            # print(Game(game['GAME_ID'], home_team, home_pts, away_team, away_pts, game['GAME_DATE'], game['TYPE']))
        
        self.schedule.add_games(games)

# team_list = []

# time_now = time.time()
# for team in teams.teams:
#     x = Team(team[1])
#     x.create_schedule()
#     team_list.append(x)

# print(time.time() - time_now)
# print(team_list)
# print(len(team_list))

team = Team('GSW')

playoff_games_hist = get_games(2021, 'Playoffs')
playoff_games_hist = playoff_games_hist[playoff_games_hist['TEAM_ABBREVIATION'] == 'GSW']
sorted_playoff_games_hist = playoff_games_hist.sort_values(by=['GAME_ID'])
sorted_playoff_games_hist = sorted_playoff_games_hist.reset_index(drop=True).get(['GAME_DATE', 'MATCHUP', 'GAME_ID', 'TEAM_ID'])
# print(sorted_playoff_games_hist)

all_series = commonplayoffseries.CommonPlayoffSeries(season=2021).get_data_frames()[0]

playoff_games_hist['SERIES_ID'] = all_series['SERIES_ID']

for playoff_game in all_series.to_dict('records'):
    
    if int(playoff_game['SERIES_ID']) // 10**1 % 10 == 1:
        print('is first round game')
        print(playoff_game['SERIES_ID'])
