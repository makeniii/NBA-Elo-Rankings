# Ideas for web app functionality

## Show all time great teams

Compile historical data to determine the highest peaks in Elo ratings. Compute Elo for historical data, saving the highest peak per season, per team. Then, display peaks by Elo. Display team name and year. Display top 30.

## Predict future games

Display win probability for future games based on current Elo only.

## Simulate season

Using the win probability for each game, use a random number generator to determine the winner of games. Do this until the end of the season.

### Apply to post season

Do the same thing but apply it to the post season.


# Ideas for web app UI

## Show win/loss streaks

If a team is on a 9-1, or better, win streak, display a hot symbol to indicate that the team *may* be better than what their Elo reflects. Similarly, the same with losing streaks.

### All-time great streaks

If a team is on a 13+ win streak, display an even hotter symbol. Similarly, do the same with a losing streak.