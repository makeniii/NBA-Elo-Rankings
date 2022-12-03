import pandas as pd
import numpy as np
import elo_system
from nba_api.stats.endpoints import leaguegamelog
from nba_api.stats.static import teams as team_list

'''
This file contains game logs from the entire 2022 playoffs. I will be using this to test my backend functions.
'''

season_id = ['22021', '22021', '22021', '22021', '52021', '52021', '52021', '52021', '42021', '42021', '42021', '42021', '42021', '42021', '42021', '42021', '42021', '42021', '42021', '42021', '42021', '42021', '42021', '42021']
team_id = [1610612751, 1610612749, 1610612744, 1610612747, 1610612751, 1610612739, 1610612737, 1610612766, 1610612748, 1610612737, 1610612748, 1610612737, 1610612755, 1610612748, 1610612748, 1610612755, 1610612748, 1610612738, 1610612738, 1610612748, 1610612744, 1610612738, 1610612744, 1610612738]
team_abbreviation = ['BKN', 'MIL', 'GSW', 'LAL', 'BKN', 'CLE', 'ATL', 'CHA', 'MIA', 'ATL', 'MIA', 'ATL', 'PHI', 'MIA', 'MIA', 'PHI', 'MIA', 'BOS', 'BOS', 'MIA', 'GSW', 'BOS', 'GSW', 'BOS']
team_name = ['Brooklyn Nets', 'Milwaukee Bucks', 'Golden State Warriors', 'Los Angeles Lakers', 'Brooklyn Nets', 'Cleveland Cavaliers', 'Atlanta Hawks', 'Charlotte Hornets', 'Miami Heat', 'Atlanta Hawks', 'Miami Heat', 'Atlanta Hawks', 'Philadelphia 76ers', 'Miami Heat', 'Miami Heat', 'Philadelphia 76ers', 'Miami Heat', 'Boston Celtics', 'Boston Celtics', 'Miami Heat', 'Golden State Warriors', 'Boston Celtics', 'Golden State Warriors', 'Boston Celtics']
game_id = ['0022100001', '0022100001', '0022100002', '0022100002', '0052100101', '0052100101', '0052100111', '0052100111', '0042100101', '0042100101', '0042100102', '0042100102', '0042100201', '0042100201', '0042100202', '0042100202', '0042100301', '0042100301', '0042100302', '0042100302', '0042100401', '0042100401', '0042100402', '0042100402']
game_date = ['2021-10-19', '2021-10-19', '2021-10-19', '2021-10-19', '2022-04-12', '2022-04-12', '2022-04-13', '2022-04-13', '2022-04-17', '2022-04-17', '2022-04-19', '2022-04-19', '2022-05-02', '2022-05-02', '2022-05-04', '2022-05-04', '2022-05-17', '2022-05-17', '2022-05-19', '2022-05-19', '2022-06-02', '2022-06-02', '2022-06-05', '2022-06-05']

matchup = ['BKN @ MIL', 'MIL vs. BKN', 'GSW @ LAL', 'LAL vs. GSW', 'BKN vs. CLE', 'CLE @ BKN', 'ATL vs. CHA', 'CHA @ ATL', 'MIA vs. ATL', 'ATL @ MIA', 'MIA vs. ATL', 'ATL @ MIA', 'PHI @ MIA', 'MIA vs. PHI', 'MIA vs. PHI', 'PHI @ MIA', 'MIA vs. BOS', 'BOS @ MIA', 'BOS @ MIA', 'MIA vs. BOS', 'GSW vs. BOS', 'BOS @ GSW', 'GSW vs. BOS', 'BOS @ GSW']
wl = ['L', 'W', 'W', 'L', 'W', 'L', 'W', 'L', 'W', 'L', 'W', 'L', 'L', 'W', 'W', 'L', 'W', 'L', 'W', 'L', 'L', 'W', 'W', 'L']
mins = [240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240]
fgm = [37, 48, 41, 45, 45, 41, 49, 34, 43, 29, 38, 41, 34, 40, 40, 38, 39, 36, 43, 38, 39, 43, 39, 30]
fga = [84, 105, 93, 95, 84, 92, 94, 90, 82, 75, 79, 87, 79, 92, 78, 84, 80, 79, 84, 86, 88, 85, 86, 80]
fg_pct = [0.44, 0.457, 0.441, 0.474, 0.536, 0.446, 0.521, 0.378, 0.524, 0.387, 0.481, 0.471, 0.43, 0.435, 0.513, 0.452, 0.488, 0.456, 0.512, 0.442, 0.443, 0.506, 0.453, 0.375]
fg3m = [17, 17, 14, 15, 9, 9, 16, 13, 18, 10, 14, 12, 6, 9, 14, 8, 10, 11, 20, 10, 19, 21, 15, 15]
fg3a = [32, 45, 39, 42, 28, 26, 32, 41, 38, 36, 36, 40, 34, 36, 29, 30, 30, 34, 40, 34, 45, 41, 37, 37]
fg3_pct = [0.531, 0.378, 0.359, 0.357, 0.321, 0.346, 0.5, 0.317, 0.474, 0.278, 0.389, 0.3, 0.176, 0.25, 0.483, 0.267, 0.333, 0.324, 0.5, 0.294, 0.422, 0.512, 0.405, 0.405]
ftm = [13, 14, 25, 9, 16, 17, 18, 22, 11, 23, 25, 11, 18, 17, 25, 19, 30, 24, 21, 16, 11, 13, 14, 13]
fta = [23, 18, 30, 19, 24, 20, 25, 29, 18, 27, 29, 14, 20, 18, 31, 22, 34, 32, 23, 22, 15, 16, 20, 17]
ft_pct = [0.565, 0.778, 0.833, 0.474, 0.667, 0.85, 0.72, 0.759, 0.611, 0.852, 0.862, 0.786, 0.9, 0.944, 0.806, 0.864, 0.882, 0.75, 0.913, 0.727, 0.733, 0.813, 0.7, 0.765]
oreb = [5, 13, 9, 5, 10, 10, 12, 11, 4, 8, 4, 7, 9, 15, 8, 5, 9, 8, 8, 12, 12, 7, 6, 6]
dreb = [39, 41, 41, 40, 33, 30, 42, 30, 36, 30, 30, 33, 28, 32, 36, 29, 30, 30, 33, 30, 27, 32, 36, 37]
reb = [44, 54, 50, 45, 43, 40, 54, 41, 40, 38, 34, 40, 37, 47, 44, 34, 39, 38, 41, 42, 39, 39, 42, 43]
ast = [19, 25, 30, 21, 33, 26, 31, 22, 35, 16, 21, 21, 18, 21, 25, 17, 18, 22, 28, 21, 24, 33, 25, 24]
stl = [3, 8, 9, 7, 9, 9, 5, 4, 12, 8, 9, 6, 4, 5, 5, 10, 10, 8, 8, 4, 8, 7, 15, 5]
blk = [9, 9, 2, 4, 9, 2, 6, 4, 3, 2, 6, 2, 6, 2, 3, 4, 12, 8, 5, 3, 6, 6, 2, 7]
tov = [13, 8, 17, 18, 14, 15, 12, 14, 15, 18, 15, 19, 15, 13, 14, 10, 13, 16, 10, 15, 14, 13, 12, 19]
pf = [17, 19, 18, 25, 20, 21, 25, 24, 22, 19, 24, 26, 17, 18, 22, 25, 24, 23, 21, 18, 16, 13, 17, 18]
pts = [104, 127, 121, 114, 115, 108, 132, 103, 115, 91, 115, 105, 92, 106, 119, 103, 118, 107, 127, 102, 108, 120, 107, 88]
plus_minus = [-23, 23, 7, -7, 7, -7, 29, -29, 24, -24, 10, -10, -14, 14, 16, -16, 11, -11, 25, -25, -12, 12, 19, -19]
game_type = ['Regular Season', 'Regular Season', 'Regular Season', 'Regular Season', 'PlayIn', 'PlayIn', 'PlayIn', 'PlayIn', 'First Round', 'First Round', 'First Round', 'First Round', 'Second Round', 'Second Round', 'Second Round', 'Second Round', 'Conference Finals', 'Conference Finals', 'Conference Finals', 
'Conference Finals', 'Finals', 'Finals', 'Finals', 'Finals']
location = ['Away', 'Home', 'Away', 'Home', 'Home', 'Away', 'Home', 'Away', 'Home', 'Away', 'Home', 'Away', 'Away', 'Home', 'Home', 'Away', 'Home', 'Away', 'Away', 'Home', 'Home', 'Away', 'Home', 'Away']
    
test_game_logs = pd.DataFrame()

test_game_logs['SEASON_ID'] = season_id
test_game_logs['TEAM_ID'] = team_id
test_game_logs['TEAM_ABBREVIATION'] = team_abbreviation
test_game_logs['TEAM_NAME'] = team_name
test_game_logs['GAME_ID'] = game_id
test_game_logs['GAME_DATE'] = game_date
test_game_logs['MATCHUP'] = matchup
test_game_logs['WL'] = wl
test_game_logs['MIN'] = mins
test_game_logs['FGM'] = fgm
test_game_logs['FGA'] = fga
test_game_logs['FG_PCT'] = fg_pct
test_game_logs['FG3M'] = fg3m
test_game_logs['FG3A'] = fg3a
test_game_logs['FG3_PCT'] = fg3_pct
test_game_logs['FTM'] = ftm
test_game_logs['FTA'] = fta
test_game_logs['FT_PCT'] = ft_pct
test_game_logs['OREB'] = oreb
test_game_logs['DREB'] = dreb
test_game_logs['REB'] = reb
test_game_logs['AST'] = ast
test_game_logs['STL'] = stl
test_game_logs['BLK'] = blk
test_game_logs['TOV'] = tov
test_game_logs['PF'] = pf
test_game_logs['PTS'] = pts
test_game_logs['PLUS_MINUS'] = plus_minus
test_game_logs['GAME_TYPE'] = game_type
test_game_logs['LOCATION'] = location

keepers = [
    'SEASON_ID',
    'TEAM_ABBREVIATION',
    'TEAM_NAME',
    'GAME_ID',
    'MATCHUP',
    'WL',
    'PLUS_MINUS',
    'GAME_TYPE',
    'LOCATION'
]

set_col = set(test_game_logs.columns.tolist())
set_keepers = set(keepers)
remove = set_col - (set_col & set_keepers)

test_game_logs.drop(columns=remove, inplace=True)

dummy_SeasonSchedule = elo_system.SeasonSchedule()
dummy_SeasonSchedule.add_games(test_game_logs)

SeasonSchedule = elo_system.SeasonSchedule()
SeasonSchedule.initialise('2021')

Teams = list()

for team in team_list.get_teams():
    Teams.append(elo_system.Team(team['full_name'], team['abbreviation']))

Season21 = elo_system.Season(2021, Teams)

Season21.schedule = SeasonSchedule

Season21.initialise_team_schedules()

bug_class = elo_system.Schedule()