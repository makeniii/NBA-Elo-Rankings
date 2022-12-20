# from nba_api.stats.endpoints import leaguegamelog
# import pandas as pd
# import numpy as np
# from abc import ABC, abstractmethod

# '''
# A few helper functions just to shorten the length of code to make it easier to read
# '''
# def get_games(season, type) -> pd.DataFrame:
#     return leaguegamelog.LeagueGameLog(season=season, season_type_all_star=type).get_data_frames()[0]

# '''
# Deciding to keep the original type(pd.DataFrame) returned from the nba api because the methods that come with
# are great and I might even use some more later down the line. Of course, I still might change it later.
# '''
# class Schedule(ABC):
#     def __init__(self) -> None:
#         self.games = pd.DataFrame() 

#     def __str__(self) -> str:
#         return str(self.games)

#     @abstractmethod
#     def add_games(self, games: pd.DataFrame) -> None:
#         self.games = pd.concat([self.games, games]).reset_index(drop=True)

#     def get_game(self, game_num) -> pd.DataFrame:
#         return self.games[self.games.index == game_num]
    
# class SeasonSchedule(Schedule):
#     # Initialise the schedule by storing all games in given season up to current date
#     def initialise(self, year):
#         games = get_games(year, 'Regular Season')
#         games = games.sort_values(by=['GAME_ID']).reset_index(drop=True)
#         games['GAME_TYPE'] = 'Regular Season'
#         playin_games = get_games(year, 'PlayIn')

#         if not playin_games.empty:
#             playin_games['GAME_TYPE'] = 'PlayIn'
#             games = pd.concat([games, playin_games])

#         playoff_games = get_games(year, 'Playoffs')

#         if not playoff_games.empty:
#             conditions = [
#                 playoff_games['GAME_ID'].str.rfind('1', 7, 8) == 7,
#                 playoff_games['GAME_ID'].str.rfind('2', 7, 8) == 7,
#                 playoff_games['GAME_ID'].str.rfind('3', 7, 8) == 7,
#                 playoff_games['GAME_ID'].str.rfind('4', 7, 8) == 7
#             ]

#             choices = [
#                 'First Round',
#                 'Second Round',
#                 'Conference Finals',
#                 'Finals'
#             ]

#             playoff_games['GAME_TYPE'] = np.select(conditions, choices, default='NOT FOUND')
#             games = pd.concat([games, playoff_games])
        
#         games['LOCATION'] = np.where(games['MATCHUP'].str.contains('vs.'), 'Home', 'Away')

#         for i in range(0, len(games.index), 2):
#             self.add_games(pd.concat([games.iloc[[i]], games.iloc[[i+1]]]).reset_index(drop=True))
        
#         self.games = self.games.sort_index(ascending=True)

#         # Remove columns that aren't used... (yet)
#         keepers = [
#             'SEASON_ID',
#             'TEAM_ABBREVIATION',
#             'TEAM_NAME',
#             'GAME_ID',
#             'MATCHUP',
#             'WL',
#             'PLUS_MINUS',
#             'GAME_TYPE',
#             'LOCATION'
#         ]

#         set_col = set(self.games.columns.tolist())
#         set_keepers = set(keepers)
#         remove = set_col - (set_col & set_keepers)
#         self.games.drop(columns=remove, inplace=True)

#         # leaguegamelog also includes games that are ongoing
#         # so remove current ongoning games that don't have fully filled columns
#         self.games = self.games.dropna()

#     def get_team_schedule(self, team_abbreviation) -> pd.DataFrame:       
#         return self.games[self.games.TEAM_ABBREVIATION == team_abbreviation]
    
#     def add_games(self, games: pd.DataFrame) -> None:
#         super().add_games(games)
#         self.games.index = pd.factorize(self.games['GAME_ID'])[0] + 1

# class TeamSchedule(Schedule):
#     def add_games(self, games: pd.DataFrame) -> None:
#         super().add_games(games)
#         self.games.index += 1

class Elo_Calculator():
    home_adv = 100
    x = 400
    elo_avg = 1500
    k = 20

    def __init__(self) -> None:
        self.elo = 1500
    
    def __repr__(self) -> str:
        return str(self.elo)

    def carry_over(self):
        self.elo = round((.75 * self.elo) + (.25 * self.elo_avg))

    def set_elo(self, Rn: int) -> None:
        self.elo = Rn

    def get_elo(self) -> int:
        return self.elo
    
    def update_elo(self, total_change: int) -> None:
        self.elo += total_change

    @staticmethod
    def win_expectancy(Ro: int, OPPRo: int, location: str) -> int:
        return 1 / (10**(-((Ro - OPPRo) + (Elo_Calculator.home_adv_calc(location)*Elo_Calculator.home_adv)) / Elo_Calculator.x) + 1)

    @staticmethod
    def w(outcome):
        return 1 if outcome == 'W' else 0

    @staticmethod
    def elo_change(Ro: int, outcome: str, OPPRo: int, location: str, mov:int):
        return  round(
                    Elo_Calculator.k * 
                    mov * 
                    (Elo_Calculator.w(outcome) - Elo_Calculator.win_expectancy(Ro, OPPRo, location))
                    )
    
    @staticmethod
    def elo(Ro: int, outcome: str, OPPRo: int, location: str, mov:int):
        return Ro + Elo_Calculator.elo_change(Ro, outcome, OPPRo, location, mov)

    @staticmethod
    def margin_of_victory(margin, RDiff, location):
        return ((margin + 3)**0.8) / (7.5 + 0.006 * (RDiff + Elo_Calculator.home_adv_calc(location)*Elo_Calculator.home_adv))

    @staticmethod
    def home_adv_calc(location: str) -> int:
        return 1 if location == 'home' else -1

# class Season():
#     # Keep track of all seasons. Maybe move to own class?
#     seasons = list()

#     def __init__(self, year, teams=[]) -> None:
#         # Year is an int of the year the season started. Might change later
#         self.year = year            
#         self.schedule = SeasonSchedule()

#         if len(self.seasons) > 0:
#             self.seasons[-1].end_season()

#         Season.seasons.append(self)

#         if len(teams) == 0:
#             raise Exception("There are no teams to create season")

#         self.teams = teams

#     def get_team(self, team_name):
#         for team in self.teams:
#             if team.name == team_name:
#                 return team
        
#         raise Exception('get_team(' + team_name + '): Team not found')
    
#     def get_team_abbreviation(self, team_abbreviation):
#         for team in self.teams:
#             if team.abbreviation == team_abbreviation:
#                 return team
        
#         raise Exception('get_team_abbreviation(' + team_abbreviation + '): Team not found')

#     def initialise_team_elos(self):
#         games = self.schedule.games

#         for i in range(0, len(games), 2):
#             team_a: Team = self.get_team_abbreviation(games.iloc[i]['TEAM_ABBREVIATION'])
#             team_b: Team = self.get_team_abbreviation(games.iloc[i+1]['TEAM_ABBREVIATION'])

#             # For each team (x2)
#             if games.iloc[i]['WL'] == 'W':
#                 winner = 0
#                 RDiff = team_a.elo.elo - team_b.elo.elo
#             else:
#                 winner = 1
#                 RDiff = team_b.elo.elo - team_a.elo.elo

#             # calculate the margin of victory (MOV)
#             mov = Elo_Calculator.margin_of_victory(games.iloc[i+winner]['PLUS_MINUS'], RDiff, games.iloc[i+winner]['LOCATION'])

#             # calculate new elo rating
#             team_a_elo_change = Elo_Calculator.calculate_elo_change(team_a.elo.get_elo(), games.iloc[i]['WL'], team_b.elo.elo, games.iloc[i]['LOCATION'], mov)
#             team_a.elo.update_elo(team_a_elo_change)
#             team_b.elo.update_elo(-team_a_elo_change)

#     def initialise_team_schedules(self):
#         for team in self.teams:
#             season_games = self.schedule.get_team_schedule(team.abbreviation)
#             season_games = season_games.reset_index(drop=True)
#             team.schedule.add_games(season_games)
    
#     def end_season(self):
#         for team in self.teams:
#             team.elo.carry_over()

#     @staticmethod
#     def get_season(year: int):
#         for season in Season.seasons:
#             if year == season.year:
#                 return season
        
#         raise Exception('No ' + str(year) + ' season')

# class Team():
    teams = list()

    def __init__(self, name, abbreviation) -> None:
        self.name = name
        self.abbreviation = abbreviation
        self.elo = Elo_Calculator()
        self.schedule = TeamSchedule()

        Team.teams.append(self)

    def __repr__(self) -> str:
        return self.name + ', aka ' + self.abbreviation + ': ' + str(self.elo)

    @staticmethod
    def get_team(team_name: str):
        for team in Team.teams:
            if team_name == team.name:
                return team
        
        raise Exception('No team named: ' + team_name)