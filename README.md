# NBA Elo Rating System

Creating my own NBA Elo rating system taking inspiration from the [NRL](https://fanalytics.weebly.com/), [Football](http://www.eloratings.net/), and [FiveThirtyEight's](https://fivethirtyeight.com/features/how-we-calculate-nba-elo-ratings/) Elo rating system. All these systems are based on [Arpad Elo's Elo rating system](https://en.wikipedia.org/wiki/Elo_rating_system) used to rate chess players.

My Elo rating system is based on the following formula:

$$\text{R}_n = \text{R}_o + \text{K} \times \text{MOV} \times (\text{W} - \text{W}_e)$$

I have a full explanation of the formula [here](docs/elo_rating_formula.md) if interested. 

The NBA Elo rating system will be web application where it displays the current Elo ratings of all NBA teams with more features to come.

I have a [diary](docs/diary.md) with a more in depth explanation and changes of the forumula, thoughts, and processes on the development of this project. It's a bit informal and rambly but I hope it provides some insight on the process.
