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
from typing import List

'''
A few helper functions just to shorten the length of code to make it easier to read
'''
def get_games(season, type) -> pd.DataFrame:
    return leaguegamelog.LeagueGameLog(season=season, season_type_all_star=type).get_data_frames()[0]

def get_games_default(type) -> pd.DataFrame:
    return leaguegamelog.LeagueGameLog(season_type_all_star=type).get_data_frames()[0]

def create_team_names() -> List[str]:
    team_list = list()

    for team in teams.teams:
        team_list.append(Team(team[1]))
    
    return team_list

class Game():
    def __init__(self, teams: pd.DataFrame):
                  # this could be changed to a dictionary with home and away keys
        self.teams = teams

    def __str__(self) -> str:
        return 'id: ' + str(self.id) + ', home_team: ' + self.home_team + ', away_team: ' + self.away_team + ', score: ' + str(self.score) + ', ' + self.date
    
    # do I need both?
    def __repr__(self) -> str:
        return str(self.teams) + '\nWeight: ' + str(self.weight) + '\n'

class RegularGame(Game):
    weight = 20

    def __init__(self, teams: pd.DataFrame):
        super().__init__(teams)

class PlayInGame(Game):
    weight = 24

    def __init__(self, teams: pd.DataFrame):
        super().__init__(teams)

class FirstRoundGame(Game):
    weight = 30

    def __init__(self, teams: pd.DataFrame):
        super().__init__(teams)

class SecondRoundGame(Game):
    weight = 40

    def __init__(self, teams: pd.DataFrame):
        super().__init__(teams)
        
class ConferenceFinalGame(Game):
    weight = 50

    def __init__(self, teams: pd.DataFrame):
        super().__init__(teams)

class FinalGame(Game):
    weight = 60

    def __init__(self, teams: pd.DataFrame):
        super().__init__(teams)

'''
Deciding to keep the original type(pd.DataFrame) returned from the nba api because the methods that come with
are great and I might even use some more later down the line. Of course, I still might change it later.
'''
class Schedule():
    def __init__(self) -> None:
        self.games = pd.DataFrame() 

    def __str__(self) -> str:
        return str(self.games)

    def add_games(self, games) -> None:
        self.games = pd.concat([self.games, games]).reset_index(drop=True)
    
class SeasonSchedule(Schedule): # Created this class simply for readability
    def __init__(self) -> None:
        super().__init__()

    def initialise(self, year):
        regular_season_games_curr = get_games(year, 'Regular Season')
        regular_season_games_curr.drop(columns=['VIDEO_AVAILABLE'], inplace=True)
        regular_season_games_curr = regular_season_games_curr.sort_values(by=['GAME_ID']).reset_index(drop=True)
        regular_season_games_curr['LOCATION'] = np.where(regular_season_games_curr['MATCHUP'].str.contains('vs.'), 'Home', 'Away')
        regular_season_games_curr['GAME_TYPE'] = 'Regular Season'
        regular_season_games_curr['ID'] = pd.factorize(regular_season_games_curr['GAME_ID'])[0] + 1
        regular_season_games_curr = regular_season_games_curr.set_index('ID')

        # print(regular_season_games_curr)

        # Duplicate game_ids are the stat lines of the two teams, so combine into one game
        for i in range(0, len(regular_season_games_curr.index), 2):
            self.add_games(pd.concat([regular_season_games_curr.iloc[[i]], regular_season_games_curr.iloc[[i+1]]]).reset_index(drop=True))

        playoff_games_curr = get_games(year, 'Playoffs')
        playoff_games_curr.drop(columns=['VIDEO_AVAILABLE'], inplace=True)

        if not playoff_games_curr.empty:
            playoff_games_curr = playoff_games_curr.sort_values(by=['GAME_ID']).reset_index(drop=True)
            playoff_games_curr['LOCATION'] = np.where(playoff_games_curr['MATCHUP'].str.contains('vs.'), 'Home', 'Away')

            conditions = [
                playoff_games_curr['GAME_ID'].str.rfind('1', 7, 8) == 7,
                playoff_games_curr['GAME_ID'].str.rfind('2', 7, 8) == 7,
                playoff_games_curr['GAME_ID'].str.rfind('3', 7, 8) == 7,
                playoff_games_curr['GAME_ID'].str.rfind('4', 7, 8) == 7
            ]

            choices = [
                'First Round',
                'Second Round',
                'Conference Finals',
                'Finals'
            ]

            playoff_games_curr['GAME_TYPE'] = np.select(conditions, choices, default='NOT FOUND')

            # Duplicate game_ids are the stat lines of the two teams, so combine into one game
            for i in range(0, len(playoff_games_curr.index), 2):
                self.add_games(pd.concat([playoff_games_curr.iloc[[i]], playoff_games_curr.iloc[[i+1]]]).reset_index(drop=True))

    def get_team_schedule(self, team) -> pd.DataFrame:
        return self.games[self.games.MATCHUP.str.contains(team)]

class TeamSchedule(Schedule):
    def __init__(self) -> None:
        super().__init__()

    def add_games(self, games) -> None:
        return super().add_games(games)

    def get_game(self, game_num) -> pd.DataFrame:
        return self.games[self.games.index == game_num]

class PR():
    def __init__(self) -> None:
        self.x = 100
        self.home_adv = 0.1
        self.pr = -1

    def win_expectancy_calc(self, Ro, OPPRo, is_home) -> int:
        return 1 / (10**(-((Ro - OPPRo) + Ro*(is_home*self.home_adv)) / self.x) + 1)

class Season():
    seasons = []                # Keep track of all seasons. Maybe move to own class?

    def __init__(self, year, teams=[]) -> None:
        self.year = year        # Year is an int of the year the season started. Might change later
        self.schedule = SeasonSchedule()
        Season.seasons.append(self)

        if len(teams) == 0:
            raise Exception("There are no teams to create season")

        self.teams = teams
    
    def initialise_schedule(self):
        self.schedule.initialise(self.year)

    def get_team(self, team_name):
        for team in self.teams:
            if team.name == team_name:
                return team
        
        raise Exception('get_team(' + team_name + '): Team not found')

class Team():
    def __init__(self, name) -> None:
        self.name = name
        self.pr = PR()
        self.schedule = TeamSchedule()

    def __repr__(self) -> str:
        return self.name
        
    def add_to_schedule(self, games):
        self.schedule.add_games(games)

    def initialise_schedule(self, seasons: List[Season]):
        for season in seasons:
            season_games = season.schedule.get_team_schedule(self.name)
            season_games = season_games.reset_index(drop=True)
            season_games['GAME_NUM'] = pd.factorize(season_games['GAME_ID'])[0] + 1
            season_games = season_games.set_index('GAME_NUM')
            self.schedule.add_games(season_games)

            # print('---------------------------------')
            # print(self.name + ' Schedule')
            # print('---------------------------------')
            # print(season_games)

        # print(self.schedule)

# team_list = []

# time_now = time.time()
# for team in teams.teams:
#     x = Team(team[1])
#     x.create_schedule()
#     team_list.append(x)

# print(time.time() - time_now)
# print(team_list)
# print(len(team_list))

# team = Team('GSW')

# playoff_games_hist = get_games(2021, 'Playoffs')
# playoff_games_hist = playoff_games_hist[playoff_games_hist['TEAM_ABBREVIATION'] == 'GSW']
# sorted_playoff_games_hist = playoff_games_hist.sort_values(by=['GAME_ID'])
# sorted_playoff_games_hist = sorted_playoff_games_hist.reset_index(drop=True).get(['GAME_DATE', 'MATCHUP', 'GAME_ID', 'TEAM_ID'])
# # print(sorted_playoff_games_hist)

# all_series = commonplayoffseries.CommonPlayoffSeries(season=2021).get_data_frames()[0]

# playoff_games_hist['SERIES_ID'] = all_series['SERIES_ID']

# for playoff_game in all_series.to_dict('records'):
    
#     if int(playoff_game['SERIES_ID']) // 10**1 % 10 == 1:
#         print('is first round game')
#         print(playoff_game['SERIES_ID'])


curr_time = time.time()

season = Season(2021, create_team_names())

season.initialise_schedule()
print(season.schedule.games)

# for team in season.teams:
#     team.initialise_schedule(season.seasons)

# team: Team = season.get_team('GSW')
# print(team.schedule.get_game(105))