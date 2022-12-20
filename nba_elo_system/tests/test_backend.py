import pytest
from .. import elo_calculator

def test_Elo_win_expectancy_calc_home():
    assert round(elo_calculator.Elo_Calculator.win_expectancy(1500, 1700, 'home'), 4) == 0.3599

def test_Elo_win_expectancy_calc_away():
    event_a = 0.3599
    event_b = 1 - event_a
    assert round(elo_calculator.Elo_Calculator.win_expectancy(1700, 1500, 'away'), 4) == event_b

def test_margin_of_victory():
    RDiff = -118
    margin = 4
    assert round(elo_calculator.Elo_Calculator.margin_of_victory(margin, RDiff, 'away'), 2) == 0.77

def test_calculate_elo_winning_team():
    location = 'home'
    OPPRo = 1400
    outcome = 'W'
    margin = 4
    Ro = 1518
    RDiff = Ro - OPPRo
    mov = elo_calculator.Elo_Calculator.margin_of_victory(margin, RDiff, location)

    assert elo_calculator.Elo_Calculator.elo(Ro, outcome, OPPRo, location, mov) == 1520

def test_calculate_elo_losing_team():
    Ro = 1400
    OPPRo = 1518
    location = 'away'
    location_win = 'home'
    outcome = 'L'
    margin = 4
    RDiff = OPPRo - Ro
    mov = elo_calculator.Elo_Calculator.margin_of_victory(margin, RDiff, location_win)

    assert elo_calculator.Elo_Calculator.elo(Ro, outcome, OPPRo, location, mov) == 1398