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
        games = get_games(year, 'Regular Season')
        games = games.sort_values(by=['GAME_ID']).reset_index(drop=True)
        games['GAME_TYPE'] = 'Regular Season'

        playin_games = get_games(year, 'PlayIn')
        playin_games.drop(columns=['VIDEO_AVAILABLE'], inplace=True)

        if not playin_games.empty:
            playin_games['GAME_TYPE'] = 'PlayIn'
            games = pd.concat([games, playin_games])

        playoff_games = get_games(year, 'Playoffs')

        if not playoff_games.empty:
            conditions = [
                playoff_games['GAME_ID'].str.rfind('1', 7, 8) == 7,
                playoff_games['GAME_ID'].str.rfind('2', 7, 8) == 7,
                playoff_games['GAME_ID'].str.rfind('3', 7, 8) == 7,
                playoff_games['GAME_ID'].str.rfind('4', 7, 8) == 7
            ]

            choices = [
                'First Round',
                'Second Round',
                'Conference Finals',
                'Finals'
            ]

            playoff_games['GAME_TYPE'] = np.select(conditions, choices, default='NOT FOUND')
            games = pd.concat([games, playoff_games])
        
        games.drop(columns=['VIDEO_AVAILABLE'], inplace=True)
        games['LOCATION'] = np.where(games['MATCHUP'].str.contains('vs.'), 'Home', 'Away')

        # Want to reorder the columns but not really bothered to do it just to swap GAME_TYPE and LOCATION

        for i in range(0, len(games.index), 2):
            self.add_games(pd.concat([games.iloc[[i]], games.iloc[[i+1]]]).reset_index(drop=True))
        
        self.games['GAME_NUM'] = pd.factorize(self.games['GAME_ID'])[0] + 1
        self.games = self.games.set_index('GAME_NUM')
        self.games = self.games.sort_index(ascending=True)

        # Remove columns that aren't used... (yet)
        keepers = [
            'TEAM_ABBREVIATION',
            'TEAM_NAME',
            'GAME_ID',
            'MATCHUP',
            'WL',
            'PLUS_MINUS',
            'GAME_TYPE',
            'LOCATION'
        ]

        set_col = set(self.games.columns.tolist())
        set_keepers = set(keepers)

        remove = set_col - (set_col & set_keepers)

        self.games.drop(columns=remove, inplace=True)

        self.games = self.games.dropna()

    def get_team_schedule(self, team_abbr) -> pd.DataFrame:
        return self.games[self.games.MATCHUP.str.contains(team_abbr)]

class TeamSchedule(Schedule):
    def __init__(self) -> None:
        super().__init__()

    def add_games(self, games) -> None:
        super().add_games(games)
        self.games['GAME_NUM'] = pd.factorize(self.games['GAME_ID'])[0] + 1
        self.games = self.games.set_index('GAME_NUM')

    def get_game(self, game_num) -> pd.DataFrame:
        return self.games[self.games.index == game_num]

class Elo():
    home_adv = 100
    x = 400
    elo_avg = 1500
    k = 20

    def __init__(self) -> None:
        self.elo = 1500

    def win_expectancy_calc(self, OPPRo: int, location: str) -> int:
        if location == 'Home':
            is_home = 1
        else:
            is_home = -1

        return 1 / (10**(-((self.elo - OPPRo) + (is_home*self.home_adv)) / self.x) + 1)

    # only using 1 or 0 because I have to get game data to see if the game went to OT. 
    # Will do in a later iteration
    def w_calc(self, outcome):
        return 1 if outcome == 'W' else 0

    def elo_calc(self, win: str, OPPRo: int, game_location: str, mov):
        self.elo = self.elo + self.k * mov * (self.w_calc(win) - self.win_expectancy_calc(OPPRo, game_location))
    
    def carry_over(self):
        self.elo = (.75 * self.elo) + (.25 * self.elo_avg)
    
    def margin_of_victory(self, margin, OPPRo, location):
        if location == 'Home':
            is_home = 1
        else:
            is_home = -1

        return ((margin + 3)**0.8) / (7.5 + 0.006 * (self.elo - OPPRo + (is_home*self.home_adv)))

class Season():
    # Keep track of all seasons. Maybe move to own class?
    seasons = list()

    def __init__(self, year, teams=[]) -> None:
        # Year is an int of the year the season started. Might change later
        self.year = year            
        self.schedule = SeasonSchedule()

        if len(self.seasons) > 0:
            self.seasons[-1].end_season()

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
    
    def get_team_abbreviation(self, team_abbreviation):
        for team in self.teams:
            if team.abbreviation == team_abbreviation:
                return team
        
        raise Exception('get_team_abbreviation(' + team_abbreviation + '): Team not found')

    def initialise_teams_elo(self):
        # For each game (x1323):
        games = self.schedule.games

        for i in range(0, len(games), 2):
            # For each team (x2)
            team_a: Team = self.get_team_abbreviation(games.iloc[i]['TEAM_ABBREVIATION'])
            team_b: Team = self.get_team_abbreviation(games.iloc[i+1]['TEAM_ABBREVIATION'])

            # calculate the margin of victory (MOV)
            if games.iloc[i]['PLUS_MINUS'] > 0:
                mov = team_a.elo.margin_of_victory(games.iloc[i]['PLUS_MINUS'], team_b.elo.elo, games.iloc[i]['LOCATION'])
            else:
                mov = team_b.elo.margin_of_victory(games.iloc[i+1]['PLUS_MINUS'], team_a.elo.elo, games.iloc[i+1]['LOCATION'])

            old_team_a_elo = team_a.elo.elo
            team_a.calculate_elo(team_b.elo.elo, games.iloc[i], mov)
            team_b.calculate_elo(old_team_a_elo, games.iloc[i+1], mov)

            if games.iloc[i]['GAME_TYPE'] == 'Finals':
                print(team_a.name + ': ' + str(team_a.elo.elo))
                print(team_b.name + ': ' + str(team_b.elo.elo))
    
    def end_season(self):
        for team in self.teams:
            team.calculate_elo_carry_over()

class Team():
    def __init__(self, name, abbreviation) -> None:
        self.name = name
        self.abbreviation = abbreviation
        self.elo = Elo()
        self.schedule = TeamSchedule()

    def __repr__(self) -> str:
        return self.name
        
    def add_to_schedule(self, games):
        self.schedule.add_games(games)

    def add_season_schedule(self, season: Season):
        season_games = season.schedule.get_team_schedule(self.abbreviation)
        season_games = season_games.reset_index(drop=True)
        self.schedule.add_games(season_games)
    
    def calculate_elo(self, opp_team_elo: int, game: pd.Series, mov):
        self.elo.elo_calc(game['WL'], opp_team_elo, game['LOCATION'], mov)
    
    def calculate_elo_carry_over(self):
        self.elo.carry_over()