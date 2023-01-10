

def add_game_to_day(game: dict, game_day: str, week_schedule: list):
    for day in week_schedule:
        if game_day == day['day']:
            if not day['games']:
                day['games'].append([game])
            elif len(day['games'][-1]) < 2:
                day['games'][-1].append(game)
            else:
                day['games'].append([game])
            
            break
    
    return week_schedule
