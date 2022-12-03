import pytest
import elo_system
import pandas as pd
from pandas.testing import assert_frame_equal
import static_game_logs as test_data
from nba_api.stats.endpoints import leaguegamelog
import json
import math

@pytest.fixture
def game_logs():
    return test_data.test_game_logs

@pytest.fixture
def SeasonSchedule():
    return test_data.SeasonSchedule

@pytest.fixture
def dummy_SeasonSchedule():
    return test_data.dummy_SeasonSchedule

@pytest.fixture
def Elo():
    Elo = elo_system.Elo()
    return Elo

@pytest.fixture
def Teams():
    return test_data.Teams

@pytest.fixture
def Season21():
    return test_data.Season21

def test_leaguegamelog():
    try:
        logs = leaguegamelog.LeagueGameLog(season=2021, season_type_all_star='Regular Season').get_data_frames()[0]
        logs = logs.iloc[[0]]
    except json.decoder.JSONDecodeError:
        raise Exception('Too many requests to NBA-api to process')

    test_log = pd.DataFrame(
        {
            'SEASON_ID': ['22021'],
            'TEAM_ID': [1610612751],
            'TEAM_ABBREVIATION': ['BKN'],
            'TEAM_NAME': ['Brooklyn Nets'],
            'GAME_ID': ['0022100001'],
            'GAME_DATE': ['2021-10-19'],
            'MATCHUP': ['BKN @ MIL'],
            'WL': ['L'],
            'MIN': [240],
            'FGM': [37],
            'FGA': [84],
            'FG_PCT': [0.44],
            'FG3M': [17],
            'FG3A': [32],
            'FG3_PCT': [0.531],
            'FTM': [13],
            'FTA': [23],
            'FT_PCT': [0.565],
            'OREB': [5],
            'DREB': [39],
            'REB': [44],
            'AST': [19],
            'STL': [3],
            'BLK': [9],
            'TOV': [13],
            'PF': [17],
            'PTS': [104],
            'PLUS_MINUS': [-23],
            'VIDEO_AVAILABLE': [1]
        }
    )

    assert_frame_equal(logs, test_log)

def test_sesaon_schedule_initialise_columns(SeasonSchedule: elo_system.SeasonSchedule):
    correct_columns = [
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

    assert SeasonSchedule.games.columns.tolist() == correct_columns

def test_sesaon_schedule_initialise_index(SeasonSchedule: elo_system.SeasonSchedule):
    correct_index = range(1, 1324)
    correct_list = [val for val in correct_index for _ in range(2)]

    assert SeasonSchedule.games.index.tolist() == correct_list

def test_SeasonSchedule_initialise_correct_game_type(SeasonSchedule: elo_system.SeasonSchedule):
    for i in range(0, len(SeasonSchedule.games)):
        game_num = int(SeasonSchedule.games.iloc[i]['GAME_ID'])

        if game_num // 10**7 % 10 == 2:
            assert SeasonSchedule.games.iloc[i]['GAME_TYPE'] == 'Regular Season'
        elif game_num // 10**7 % 10 == 5:
            assert SeasonSchedule.games.iloc[i]['GAME_TYPE'] == 'PlayIn'
        elif game_num // 10**7 % 10 == 4:
            if game_num // 10**2 % 10 == 1:
                assert SeasonSchedule.games.iloc[i]['GAME_TYPE'] == 'First Round'
            if game_num // 10**2 % 10 == 2:
                assert SeasonSchedule.games.iloc[i]['GAME_TYPE'] == 'Second Round'
            if game_num // 10**2 % 10 == 3:
                assert SeasonSchedule.games.iloc[i]['GAME_TYPE'] == 'Conference Finals'
            if game_num // 10**2 % 10 == 4:
                assert SeasonSchedule.games.iloc[i]['GAME_TYPE'] == 'Finals'
        else:
            assert False

def test_SeasonSchedule_initialise_correct_location(SeasonSchedule: elo_system.SeasonSchedule):
    for i in range(0, len(SeasonSchedule.games)):
        if 'vs.' in SeasonSchedule.games.iloc[i]['MATCHUP']:
            assert SeasonSchedule.games.iloc[i]['LOCATION'] == 'Home'
        elif '@' in SeasonSchedule.games.iloc[i]['MATCHUP']:
            assert SeasonSchedule.games.iloc[i]['LOCATION'] == 'Away'
        else:
            assert False

def test_season_get_team_schedule(dummy_SeasonSchedule):
    assert_frame_equal(dummy_SeasonSchedule.get_team_schedule('Brooklyn Nets'), dummy_SeasonSchedule.games.iloc[[0, 4]])

def test_SeasonSchedule(SeasonSchedule, dummy_SeasonSchedule):
    assert_frame_equal(SeasonSchedule.get_game(2), dummy_SeasonSchedule.games.iloc[[2, 3]])

def test_Elo_win_expectancy_calc_home(Elo: elo_system.Elo):
    assert round(Elo.win_expectancy_calc(1700, 'Home'), 4) == 0.3599

def test_Elo_win_expectancy_calc_away(Elo: elo_system.Elo):
    event_a = 0.3599
    event_b = 1 - event_a
    Elo.elo = 1700
    assert round(Elo.win_expectancy_calc(1500, 'Away'), 4) == event_b

def test_margin_of_victory(Elo: elo_system.Elo):
    assert round(Elo.margin_of_victory(4, 1618, 'Away'), 2) == 0.77

def test_calculate_elo(Elo: elo_system.Elo):
    location = 'Away'
    OPPRo = 1600
    win = 'W'
    margin = 13

    Elo.calculate_elo(win, OPPRo, location, Elo.margin_of_victory(margin, OPPRo, location))

    assert Elo.elo == 1522