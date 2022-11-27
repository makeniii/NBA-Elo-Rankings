import pytest
import elo_system
import pandas as pd
import static_game_logs as test_data
from nba_api.stats.endpoints import leaguegamelog

@pytest.fixture
def game_logs():
    return test_data.test_game_logs

@pytest.fixture
def season_schedule():
    return test_data.season_schedule

@pytest.fixture
def dummy_season_schedule():
    return test_data.dummy_season_schedule

def test_sesaon_schedule_initialise_columns(season_schedule: elo_system.SeasonSchedule):
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

    assert season_schedule.games.columns.tolist() == correct_columns

def test_sesaon_schedule_initialise_count(season_schedule: elo_system.SeasonSchedule):
    correct_index = range(1, 1324)
    correct_list = [val for val in correct_index for _ in range(2)]

    assert season_schedule.games.index.tolist() == correct_list

def test_season_schedule_initialise_correct_game_type(season_schedule: elo_system.SeasonSchedule):
    for i in range(0, len(season_schedule.games)):
        game_num = int(season_schedule.games.iloc[i]['GAME_ID'])

        if game_num // 10**7 % 10 == 2:
            assert season_schedule.games.iloc[i]['GAME_TYPE'] == 'Regular Season'
        elif game_num // 10**7 % 10 == 5:
            assert season_schedule.games.iloc[i]['GAME_TYPE'] == 'PlayIn'
        elif game_num // 10**7 % 10 == 4:
            if game_num // 10**2 % 10 == 1:
                assert season_schedule.games.iloc[i]['GAME_TYPE'] == 'First Round'
            if game_num // 10**2 % 10 == 2:
                assert season_schedule.games.iloc[i]['GAME_TYPE'] == 'Second Round'
            if game_num // 10**2 % 10 == 3:
                assert season_schedule.games.iloc[i]['GAME_TYPE'] == 'Conference Finals'
            if game_num // 10**2 % 10 == 4:
                assert season_schedule.games.iloc[i]['GAME_TYPE'] == 'Finals'
        else:
            assert False

def test_season_schedule_initialise_correct_location(season_schedule: elo_system.SeasonSchedule):
    for i in range(0, len(season_schedule.games)):
        if 'vs.' in season_schedule.games.iloc[i]['MATCHUP']:
            assert season_schedule.games.iloc[i]['LOCATION'] == 'Home'
        elif '@' in season_schedule.games.iloc[i]['MATCHUP']:
            assert season_schedule.games.iloc[i]['LOCATION'] == 'Away'
        else:
            assert False

