import pytest
import elo_system
import pandas as pd
import static_game_logs as test_data
from nba_api.stats.endpoints import leaguegamelog

@pytest.fixture
def game_logs():
    return test_data.test_game_logs

