# NBA Elo Rating System

## Description

Creating my own NBA Elo rating system taking inspiration from the [NRL](https://fanalytics.weebly.com/), [Football](http://www.eloratings.net/), and [FiveThirtyEight's](https://fivethirtyeight.com/features/how-we-calculate-nba-elo-ratings/) Elo rating system. All these systems are based on [Arpad Elo's Elo rating system](https://en.wikipedia.org/wiki/Elo_rating_system) used to rate chess players.

My Elo rating system is based on the following formula:

$$\text{R}_n = \text{R}_o + \text{K} \times \text{MOV} \times (\text{W} - \text{W}_e)$$

I have a full explanation of the formula [here](docs/elo_rating_formula.md) if interested. 

The NBA Elo rating system will be web application where it displays the current Elo ratings of all NBA teams with more features to come.

I have a [diary](docs/diary.md) with a more in depth explanation and changes of the forumula, thoughts, and processes on the development of this project. It's a bit informal and rambly but I hope it provides some insight on the process.

## Installation

```bash
git clone https://github.com/makeniii/NBA-Elo-Rankings.git
pip install -r requirements.txt
```

## Usage

Please be aware, when first starting the server, initialising the SQLite database takse approximately 8 minutes on my machine. Times may vary on different machines. There is a progress bar which roughly displays the time taken and the ETA. It looks like the following,

```bash
[elapsed time: 0:05:48] |*********************************************                | (ETA:  0:01:48)
```

### Windows

To run the server:
```bash
py run.py
```

### Linux/macOS

To run the server:
```bash
python3 run.py
```

### Website Access

To access the website, go to: 
```
localhost:5000
```

or <a href="http:localhost:5000">click here<a/>.

## Acknowledgements

I was able to find icons thanks to [Bharat Icons](https://www.flaticon.com/free-icons/basketball).

Thanks to the developers of [nba_api](https://github.com/swar/nba_api).

Again, I've taken a lot of the formulation from [FiveThirtyEight's](https://fivethirtyeight.com/features/how-we-calculate-nba-elo-ratings/) model, and to a lesser extent, these [Football](http://www.eloratings.net/) and [NRL](https://fanalytics.weebly.com/) models. The rest of the formula is from [Arpad Elo's Elo rating system](https://en.wikipedia.org/wiki/Elo_rating_system).

## NBA.com

NBA.com has a [Terms of Use](https://www.nba.com/termsofuse) regarding the use of the NBA’s digital platforms.