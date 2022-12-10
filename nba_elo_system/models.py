from nba_elo_system.elo_system import SeasonSchedule, TeamSchedule, Elo, Season, Team
from nba_api.stats.static import teams as team_list

teams = list()

for team in team_list.get_teams():
    teams.append(Team(team['full_name'], team['abbreviation']))

season_21 = Season(2021, teams)
season_21.schedule.initialise(season_21.year)
season_21.initialise_team_schedules()
season_21.initialise_team_elos()

season_22 = Season(2022, teams)
season_22.schedule.initialise(season_22.year)
season_22.initialise_team_schedules()
season_22.initialise_team_elos()