# 5/11/22

## Formula Explanation

Trying to come up with a modified version of the Elo ranking system based on the NRL and Football power rankings.

Starting from here:
> $$\text{R}_n = \text{R}_o + \text{K} \times (\text{W} - \text{W}_e)$$

$\text{R}_n =$ New PR

$\text{R}_o =$ Pre Match PR

$\text{K} =$ Variable

$\text{W} =$ Result of Game

$\text{W}_e =$ Expected Result

To further clarify some of the independant variables.

### K

There two factors to take into consideration for calculating $\text{K}$:
- What type of game is it? (Finals/Conference Finals/Regular Season etc.)
- Score difference

I've come up with these constants for what game is being played. For games being played in the playoffs, opponent teams are better and the deeper you go, the better the teams _should be_.

| Type | Value |
| ---- | ----- |
| Finals | 60 |
| Conference Finals | 50 |
| 2nd Round Playoffs | 40 |
| 1st Round Playoffs | 30 |
| Play In | 24 |
| Regular Season | 20 |

As for score difference, deciding to have it not affect $\text{K}$ as of now. Just to make starting easier. I do wonder how I will decide this. The Grizzlies just beat the Thunder by 73 points last season (21-22) for an NBA record. 

Going on a little tangent, taking this game by itself, and you might think that the Grizzlies might be the best NBA team. It's somewhat true because they did finish in 2nd in the Western Conference and also with the second best record across the NBA, but they fell to the eventual champs in the second round of the playoffs, 4-2. There are so many factors to why a team would get blown out like this. Interesting thing is that the Grizzlies were playing without Ja Morant, their "Superstar" that year. The Grizzlies went [20-5](https://www.statmuse.com/nba/ask?q=grizzlies+record+without+ja+morant+2021-22) without and [36-21](https://www.statmuse.com/nba/ask?q=grizzlies+record+with+ja+morant+2021-22) with Ja. Even advanced statistics supported this. With Ja, their [OFFRTG was 114.5](https://www.statmuse.com/nba/ask?q=grizzlies+offensive+rating+with+ja+morant+2021-22)([#10](https://www.statmuse.com/nba/ask?q=team+offensive+rating+2021-2)*) and their [DEFRTG was 112.3](https://www.statmuse.com/nba/ask?q=grizzlies+offensive+rating+with+ja+morant+2021-22)([T#15](https://www.statmuse.com/nba/ask?q=team+defensive+rating+2021-22)) for a NETRTG of 2.2+([T#12](https://www.statmuse.com/nba/ask?q=team+net+rating+2021-22)). Without Ja, thier [OFFRTG was 117.6](https://www.statmuse.com/nba/ask?q=grizzlies+offensive+rating+without+ja+morant+2021-22)([#1](https://www.statmuse.com/nba/ask?q=teams+net+rating+2021-22)) and thier [DEFRTG was 104](https://www.statmuse.com/nba/ask?q=grizzlies+defensive+rating+without+ja+morant+2021-22)([#1](https://www.statmuse.com/nba/ask?q=teams+net+rating+2021-22)) for a NETRTG of 13.6+([#1](https://www.statmuse.com/nba/ask?q=teams+net+rating+2021-22)). This trend also continues into the playoffs. With Ja, their [OFFRTG was 111.7](https://www.statmuse.com/nba/ask?q=grizzlies+net+rating+with+ja+morant+2021-22+playoffs)([#8](https://www.statmuse.com/nba/ask?q=teams+net+rating+2021-22+playoffs)) and their [DEFRTG was 110.9](https://www.statmuse.com/nba/ask?q=grizzlies+net+rating+with+ja+morant+2021-22+playoffs)([#5](https://www.statmuse.com/nba/ask?q=teams+net+rating+2021-22+playoffs)) for a NETRTG of 0.8+([T#5](https://www.statmuse.com/nba/ask?q=teams+net+rating+2021-22+playoffs)). Without Ja, their [OFFRTG was 108.7](https://www.statmuse.com/nba/ask?q=grizzlies+net+rating+without+ja+morant+2021-22+playoffs)([#12](https://www.statmuse.com/nba/ask?q=teams+net+rating+2021-22+playoffs)) and their [DEFRTG was 101.4](https://www.statmuse.com/nba/ask?q=grizzlies+net+rating+without+ja+morant+2021-22+playoffs)([#1](https://www.statmuse.com/nba/ask?q=teams+net+rating+2021-22+playoffs)) for a NETRTG of 7.3+([#1](https://www.statmuse.com/nba/ask?q=teams+net+rating+2021-22+playoffs)).

\* I'm taking the ratings and comparing them to the other 29 teams in the NBA. Obviously, comparing a smaller sample size to the rest of the NBA doesn't make these statements true. But, it does paint an intreseting picture. This also applies to the rest of the comparisons, doubly so for the playoffs since there are much fewer games.

Not sure why I went on a Memphis rant. Now, returning to my original point, I think that a team beating seven opponents in a row by a point differential of 10 is more impressive than winning by 70 for a single game. I think that consistancy means more for how good a team is rather than these anomalies. Not sure yet to how I could reward teams with a high point differential but it's something to think about in the future. Also, I should probably add a cap to the point of how much the point differential will affect $\text{K}$. Thinking of something around 20.

### W

I tried to have $\text{W}$ set according to the following table:

|Time|Win|
|---|---|
|Regulation|1+/-|
|OT|0.65+/-|
|OT2|0.6125+/-|
|OT3|0.575+/-|
|OT4|0.5375+/-|

So for example, if you win during regulation time, $\text{W}$ is set to 1 and the losing team will have W set to -1 and so on. But I realised that $\text{W}_e$ could not calculate if a game would go double/triple/quadruple overtime since it only returns a percentage.

So I just set W to:

$$ 
\text{W} =
  \begin{cases}
    \displaystyle 1 & \quad \text{a win} \\
    \displaystyle 0.5 & \quad \text{goes OT} \\
    \displaystyle 0 & \quad \text{a loss}
  \end{cases}
$$

Might use zero sum in the future if PR progresses too slowly. Something like:

$$ 
\text{W} =
  \begin{cases}
    \displaystyle 1 & \quad \text{a win} \\
    \displaystyle 0.5 & \quad \text{a win in OT} \\
    \displaystyle -0.5 & \quad \text{a loss in OT} \\
    \displaystyle -1 & \quad \text{a loss}
  \end{cases}
$$

Could always multiply $\text{W}$ by a constant to accerlate even further.

### W<sub>e

$\text{W}_e$ is calculated using this formula:

$$\frac{1}{10^{-\frac{\text{RDiff}+\text{HomeAdv}}{x}}+1}$$

Where $\text{RDiff}$ is the difference in PR. The expected result is always $\geq 0 \text{ and} \leq 1$. This is because even though there is a 100+/- difference in PR, a team is **never** guaranteed a win/loss.

$\text{HomeAdv}$ is a constant. After reading a [post](https://bleacherreport.com/articles/1520496-how-important-is-home-court-advantage-in-the-nba#:~:text=Of%20the%20four%20major%20American,games%20in%20their%20home%20arenas.), I've decided to make home court advantage worth 10%. The article mentions that there is a discrepency between the regular season and playoffs home court advantages. ~61% of home teams in the regular season win, while ~65% of home playoff teams win. The article does say that teams that home teams in the playoffs are always the higher seed so there is that to take into consideration. So, that's why I decided to make home teams 10% better, thus making $\text{HomeAdv}=\text{R}_\text{o}\times0.1$. Although, this does introduce the fact that higher PR teams will gain more from home court. However, it does make sense to me that better teams gain more from home court.

$x$ is just a coefficient used to scale how fast/slow the win expectancy changes. I've set it currently to 50. Will probably change in the future.

Finally, here is what the full formula looks like:

$$\text{R}_n=\text{R}_o+\text{K}\times\left(\text{W}-\frac{1}{10^{-\frac{\text{RDiff}+(\text{R}_o\times0.1)}{x}}+1}\right)$$

Added a new branch, testing, for exactly that, testing. Added a win expectancy calculator based on what I currently have formulated. Hopefully I stick to this branch when testing.

Next, I need to figure out the scope of this project. I have a rough idea that I want a website(local) visually showing me the power rankings. Probably start with a simple text based version before moving to a visual (graph?) representation of the rankings. There are many different features that can be added to this like a predictor for NBA champs, ladder etc.

Also, figure out what programming language to use. It'll be easier for me to tweak and test the formula once it's been coded than using pen and paper to check.

Going to log the time spent on this project.

Time: 6:00

\* All times are an approximation formatted as hh:mm

# 6/11/22

> Also, figure out what programming language to use.

I've decided that the programming language I'll primarily use is python3.9 (it's what's installed on my pc) with javascript - well probably - for the website side. Created the project in github to keep track of issues and added the first issue which was to decide on a programming language. Completed that obviously. Now, moving on to what milestones I should set for the project. After thinking and writing down some ideas, the first milestone should be the backend with a simple implementation of the formula I currently have. The second milestone would be a simple website that displays the information as a chart. From there I can add more features and complexities to it.

Created 2 milestones and added all(?) tasks for the simple backend milestone. Added tags that show priority from high, medium to low. High being I have to complete the task for the core program to work as intended. Meduium being something I _want_ to complete and low being something I can complete if I feel like it. I'm able to sort what tasks are connected by milestone then by the numbering of the title. So for example, must complete task 1.3 before completing task 1 or task 1.3.5 before task 1.3 and so on.

> I need to figure out the scope of this project.

As for the scope of the project, I feel like this is something I can continueously build upon as I think of more features or improvements to like the aesthetics of the website. So, I guess the scope is as big as I want it to be. Currently have 2 milestones set and will work from there. This does mean that once I complete these first two milestones, every new feature after that will have a medium or low priority. Not sure if that makes sense but it does to me, so, going to roll with it. So, yeah, every feature will be it's own milestone.

After adding my 2 milestones, I've thought about how I want to organise the new code I'll be writing. I've come up with adding a new branch for every milestone. Since every milestone is a feature or just about, I think that having the ability to test, tweak, or fix features without touching the main branch is great because that means I _should_ be able to work on multiple features simultaneously - I hope.

> Added a new branch, testing, for exactly that, testing. Added a win expectancy calculator based on what I currently have formulated. Hopefully I stick to this branch when testing.

That means, that my testing branch is now useless since I'll be doing the testing in their own branches.

I spent a long time thinking about how I'm going to approach my solution. At first I didn't take into consideration how I'm going to program, whether I'd be using a simple top down approach or something like OOP. I will admit that my OOP knowledge is not the best, but after thinking for a while about how my will hypothetically be, I realised that I will probably end up with classes anyways. So, I'm going to try and also, hopefully, improve my OOP skills. Also, OOP was something I didn't even take in to account when considering what programming language to use. Luckily, I can still use OOP in Python.

After a bit, I finally have my starting class diagram:
  
![draft class diagram](https://user-images.githubusercontent.com/117491084/200154248-8a2bcf1e-e941-416f-b48d-65d862e6244c.png)

Notation is probably wrong but to me, it looks like a decent class diagram that anyone - with class diagram knowledge - would understand. There'll for sure be many edits to the diagram to come, and yes, I've already made one. Will probably also add more detail too, like adding input variables.
  
Something I also need to do is cut some of the formula information from here and add it to the readme file.

I spent around 2 hours wasting time because I couldn't get the nba-api to install. First it was showing me an error that was saying that the subprocess was failing and not pip iteself. I tried to diagnose the problem but it ended up no where. So after around 2 hours, I decided to uninstall mingw64 - honestly don't even remember why I installed it, but it was probably for one of my courses - and freshly install python 3.9.13. Oh my days, it finally worked. I made a new venv and activated it and finally installed nba-api. I really wasted that time.

I implemented the game class with a few changes. Will need to update class diagram to reflect those changes. I added an id field to the game class just in case I need to use it in the future. I also implemented some of the functionality of issue 2.1.1. That's without testing though. I also did have to install pandas to use dataFrames.
  
Time: 6:00
  
# 7/11/22

Continuing where I left off, yesterday I was able to get all NBA games for the 2021-22 season that includes; home, away, pts for both teams, and date. With this, I can complete all but the game type entry.
  
Well I ran into a small problem, none of the functions in the nba-api returns data on playoff series

# 8/11/22

Fell asleep at the computer yesterday. So, I had a little problem where I couldn't dynamically get the season based on the current date. I finally solved that. Now I'm able to create a schedule up to the teams last played game, which includes the previous season too.

I added a TeamSchedule subclass of Schedule becuase I realised that team schedules and season schedules would be different. Team schedules will include things like whether they won or not whereas season schedules will just include game data not specific to a team. So, I finally compeleted 2.1.1 but without any extensive testing. Just based on print statements, it appears to be correct. Now I can create a schedule for every team in the nba up til their last played game, including the previous season. Will need to do the same for when I implement the Season class. But that will be much easier since I will just be creating games and not having to manipulate data. It will be similar to Team.create_schedule anyways.
  
Welp, the nba server thinks I'm a bot and has at least suspended my ip. I can't recieve any data for the time being. I guess looping through all nba teams and creating the schedules was too much for the server. Hopefully it works fine later today or tomorrow.

Actually, I fixed the problem by adding a 2 second sleep - someone had the same problem - after each call to the api. Creating the schedules for every team would mean that 2 minutes of execution would be added which isn't great. I added a simple time calculator to see how long it would take and it took 4 minutes and 14 seconds just create the schedules. I lowered the sleep time to 1 second and that reduced the time to 2 minutes and 14 seconds. So, while 2.1.1 is complete - again not tested - the time it takes to execute is high I think. I think a better solution would just have a total of 4 requests to get the data which would be the season logs and store it somewhere for the program to access. For now I think it would be easier to just store it in a variable in the program at the moment if I do go that route. So that's 2.1 done.

Implemented a PR class which will handle all the PR calculations and store the PR of the team. Completed 2.2.1 since it's a mathematical equation, I only need to check one example to know if it's correct because there are no cases to consider with numbers.

2.2.2 is a tricky because while I do have a game type, it doesn't tell me which one row the game belongs as seen here:

| Type | Value |
| ---- | ----- |
| Finals | 60 |
| Conference Finals | 50 |
| 2nd Round Playoffs | 40 |
| 1st Round Playoffs | 30 |
| Play In | 24 |
| Regular Season | 20 |

I did find a function that returns a playoff series ID. Going to have to check if I'm able to use this to sort the games to what type they are.

So, I am able to get the type of game for playoff games by using the series_id. This is great news. It makes it much easier for me now.
  
Now, back to what I said a bit earlier:

> I think a better solution would just have a total of 4 requests to get the data which would be the season logs and store it somewhere for the program to access.

I think that a solution to this problem would be to implement the season class, and then make the schedule. From there, make the team schedules from the season schedule that way I only have to use 2 api requests per season. In this case, I'll be only making 4 requests to the api to get the previous and current season games and playoff games. I'm also thinking of adding a playoff subclass to games, maybe even more subclasses like first round subclass and so on because that will make it even easier to have the value they are worth for the $\text{K}$ calculation because then I'll only need to change one line if the values were to change. Will also add a subclass of game to be a team specific game. So the data in that class will be specific to a team, so the plus minus field will be according to that team and the W/L will also be according to that team too. Once I refactor the code in `Team.create_schedule()`, it'll be much easier to read.

Time: 6:00

# 10/11/22

I implemented subclasses for the type of game being played (e.g. first round playoff game, play in game etc.). I added a weight attribute to `Game` which is what value the type of game is being played. Next, I will try to implement the `Season` class where it will create the schedule and from there, all teams can filter out the games that their team is playing so that I don't have to call the api too often and cause it to be slow. The api will only be called in the `Season` class when creating the schedule and not the `Team` class. Also, this means that there is a memory savings because there will be less copies of the same game saved in different locations.

I set `Schedule` to store a `DataFrame` at first because of the useful methods I might want to use in the future and also the fact that the api returns the same type so it would be easier to just store it as is. So, while I was rewriting my code, I was able to remove ~100 lines total, of code from `Season.create_schedule()` and `Team.create_schedule()`. But then I realised that I would have to add to the `DataFrame` to store the weight of the type of game being played. Also, that the `Game` class and subclasses become obsolete now that it is not a part of any class. I guess I'm going to revert my code a bit.

I'm currently in the process of refactoring my code again. I changed `Game` to store a `dict`, where the `HOME` key wouold store the `DataFrame` of the home team and the same for the away team. Now, I can have only one copy of the game in the season schedule and games are no longer repeating. However, execution time is pretty long compared to the previous solution I had.

> I set `Schedule` to store a `DataFrame`...

The code I currently have is much slower in comparison to the other solution where we were only dealing with `DataFrame` objects. The main reason why I prefer this design over the other is the fact that it is easier to understand the code from a person who isn't me.

# 11/11/22

> The code I currently have is much slower in comparison to the other solution where we were only dealing with `DataFrame` objects. The main reason why I prefer this design over the other is the fact that it is easier to understand the code from a person who isn't me.

You know, I'm not sure if I should prioritise speed or readability. But, I'll make the decision once I fully refactor `Season.create_schedule` and `Team.create_schedule`. It's just a really hard decision. I'm not the best with OOP at the moment - my knowledge is a bit fuzzy because it has been a while now since I studied the unit at university.

I'm actually going to keep `DataFrames` as the main object which keeps the schedule of the sesaon. So, from:

```
Schedule.games = List[Game]
```

To:

```
Schedule.games = pd.DataFrame
```

Hopefully, in the future when the application gets a bit more complicated, the change will be more advantageous.

Actually, I take that back. I realised that the weight attribute wouldn't really make sense to be a part of the `DataFrame`. There is also the fact that it would be cleaner to have a class attribute weight because changing the one variable means a change to the functions that are using the attribute so it's much easier.

Flip-flopped again. I changed:

```
Schedule.games = List[Game]
```

To:

```
Schedule.games = pd.DataFrame
```

Hopefully this is the last time I change this but I doubt it. In the future I'll probably refactor the code again. Still haven't finished implementing the changes to both `Team` and `Season`.

# 16/11/22

Start: 11:30am

To start off with, I forgot to push and add to my diary on the 12/11/22. Guess working on the project til I fall asleep is not a great idea. I did make some major changes to the formula though. 

I guess I never really thought about the range of $\text{R}_n$. I orginally had plans for $\text{R}_n, 0 \leq \text{R}_n \leq 100$, but from the original formula, you can see that there nothing enforcing the range for the function. I had just thought that I'll scale $\text{R}_n$ to $0 \leq \text{R}_n \leq 100$. Which is something that I'll probably still do because I think that ratings between $0$ and $100$ is more intuitive than ratings in the thousands. This is something I'll come back to though. The problem with what I had before was that I was thinking, coding, and testing $\text{R}_n$ in terms of ratings between $0$ and $100$ instead of $1000\text{s}$. 

Now the next problem is how do I scale $\text{R}_n$ to $\text{R}_n, 0 \leq \text{R}_n \leq 100$ without knowing the start and endpoints of the scale. [This post from FiveThrityEight](https://projects.fivethirtyeight.com/complete-history-of-the-nba/#warriors) show us that according to their Elo rating system, the highest elo achieved was by the 17 Golden State Warriors. With an Elo of $1865$ they had surpassed the 96 Chicago Bulls' $1853$. No surprise there really. Greatest team of all time should have the highest Elo rating. [Here](https://fivethirtyeight.com/features/how-we-calculate-nba-elo-ratings/), FiveThirtyEight explains their NBA Elo system and they include a table that shows how an Elo would roughly translate to record and team description. With the Warriors and their rating of $1865$, it would translate to an all time great time, which they were. They go as low as $1200$ which would be a historically awful team. Now, back to the scale. I think I should set the upper limit $1900$ and the lower limit to $1100$. Of course, this can change if there is a team that actually goes above/below this.

From using the two points, $(1100, 0)$ and $(1900, 100)$. The linear formula to scale $\text{R}_n$ is:
$$f(x) = \frac{1}{8}x -\frac{275}{2}$$

Not going to scale $\text{R}_n$ until it's time to display to users because then there's less confusion of whether it's scaled or not and I would only have scale once. So I'll need to now implement this scale function in the `PR` class.

Next, I changed the $\text{W}_e$ formula a bit. Now,

$$ 
\text{HomeAdv} =
  \begin{cases}
    \displaystyle 100 & \quad \text{home game} \\
    \displaystyle 0 & \quad \text{away game}
  \end{cases}
$$

Where it was previously, $\text{HomeAdv}=\text{R}_\text{o}\times0.1$. Now that I've realised that the Elo ratings are as high as 1800, the $0.1$ multiplier for $\text{HomeAdv}$ is quite a lot. The [FiveThirtyEight](https://fivethirtyeight.com/features/how-we-calculate-nba-elo-ratings/) and [Football](http://www.eloratings.net/about) rating systems both use a constant of $100$ to equate home advantage. I'm not a mathematician so I'll stick with $100$ too.

Lastly, I set `PR.pr = 1500`. From what I've searched and from [FiveThirtyEight](https://fivethirtyeight.com/features/how-we-calculate-nba-elo-ratings/), the average Elo rating is $1500$. So, that's why I set the default rating to $1500$.

Now, moving on to current changes.

I've realised that I'm probably using the wrong termanology when I have a `PR` attribute named `pr` instead of `elo` because the power ranking is based on Elo. The power rankings is just team standings based on Elo. So, I'm going to change that to attribute to `elo`. Actually, it really applies to the whole class. I renamed the `PR` class and attribute to `Elo` and everything else that had `pr` in the name.

I'm currently trying to implement an efficient method to initialise all teams Elo rating. The fastest way seems to be through pandas vectorization or numpy vectorization. But before that, I found a little error in my $\text{W}_e$ calculations. I found that the $\text{HomeTeam W}_e + \text{AwayTeam W}_e \neq 1$. This obviously is wrong. I found that the reason why it was wrong, was because I didn't account for the fact the the $\text{RDiff}$ when calculating for an away team would have to include $100$ points for the home team advantage. It was an easy fix though.

Back to vectorization, I couldn't figure out how to use vectorization for `Season.initialise_teams_elo()`. So, I just use a for loop with a step of 2. Probably come back to this to maybe find a more efficient way of doing this.

I modified:
```
Team.initialise_schedule(seasons: List[Season])
```

to:
```
Team.add_season_schedule(season: Season)
```

I did this because it was easier to add other seasons once the team schedule was initialised. Using the old method would replicate games because it would iterate through all seasons to add games.

I've adjusted the value of $\text{K}$ depending on the game that is being played. It will probably change again later on.

I've found a way to account for the margin of victory thanks to [FiveThirtyEight](https://fivethirtyeight.com/features/how-we-calculate-nba-elo-ratings/). I'm going to try and implement this now instead of later.

I've implemented the margin of victory calculator for the `Elo` class. Unfortunately, it isn't as clean as I would have hoped. Function could use a refactor later on. 

Earlier I said,
> I've come up with these constants for what game is being played. For games being played in the playoffs, opponent teams are better and the deeper you go, the better the teams _should be_.
>| Type | Value |
>| ---- | ----- |
>| Finals | 60 |
>| Conference Finals | 50 |
>| 2nd Round Playoffs | 40 |
>| 1st Round Playoffs | 30 |
>| Play In | 24 |
>| Regular Season | 20 |

I was completely wrong. $\text{K}$ having a higher value the further into the playoffs actually less makes sense to me because the higher $\text{K}$ is, the more variance $\text{R}_n$ would have. So, I've adjusted the value of $\text{K}$ to $$\text{K} = 20$$

I took [FiveThirtyEight's](https://fivethirtyeight.com/features/how-we-calculate-nba-elo-ratings/) $\text{K}$ value and after some testing and trying different values, I decided on that value. Not because the people behind FiveThirtyEight are smarter than me. Also, FiveThirtyEight has a Elo ratings to point spread formula which definitely be useful in the future. 

So, now that the margin of victory is implemented, that means that the formula has now changed to accomodate this change. The formula now is:

$$\text{R}_n=\text{R}_o+\text{K}\times\text{MOV}\times\left(\text{W}-\frac{1}{10^{-\frac{\text{RDiff}+\text{HomeAdv}}{x}}+1}\right)$$

I've finally deleted the `Game` class and it's subclasses. It'll be easy to re-do if I need to so nothing is really lost.

So, that's all for the first milestone, which is the backend of the app. Now, all that I need to do to complete it, is to code a testing suit for the main functions.

End: 6:30pm

# 17/11/22

Start: 9:30pm

I found a back-up to the NBA api if there's something I can't do on there. It's the [basketball reference scraper](https://github.com/vishaalagartha/basketball_reference_scraper). Basically as the name suggests, it's a web scraper for the [basketball reference](https://www.basketball-reference.com/). Why would I need this over the NBA api? Well, because the NBA api blocks users after too many rapid calls (~3-4 calls in short succession) and I _don't think_ it has future schedules which would be something that would be important if I ever try to predict outcomes of future games based on Elo ratings.

There's an ESPN api but I'm not too confident in that. There doesn't seem to be much info or users of this api when I search "ESPN api" on google so it's not looking promising. Really the only comment I found on it was that it was terrible. But again, it does have a schedule endpoint which would be useful.

Lastly, I found another NBA library, but this time the library pulls information from both nba stats and data nba. It has been archived so the data and maybe even the functions are out of date and won't work anymore. I saw a comment that because It hasn't been updated in a while, the data only goes up to OCT 2020 which is quite outdated for what I'm _currently_ doing. Maybe I could still make use of this library down the line if I needed stats from before 2021 and other options were exhausted.

End: 10pm

# 18/11/22

Start: 8:45pm

I tried to organise my testing suite and my current code by separating the code into folders. So adding something like a backend, frontend, and test folder etc. But, when I created my test file, I tried to import my code using relative imports but it just wouldn't work. Hopefully I either find a fix for this later on or if I just use the root directory, the code base doesn't get too big. I did rename my file main file and added new ones though.

Not sure how I spent two hours but I was only able to get a static record(panda.Dataframe) of the playoff games in the 2022 season. Well I actually am sure of how. I spent time going back and forth from another short program that I wrote to take in lines of input, each line is a new element in an array, and at the end, print the array. Copy and paste the output from the program and paste it into the test file to create a static list to add to the Dataframe. I realise around a third of the way, that I could just easily just iterate over the columns and convert each column into a list to make it easier than using the useless program that I wrote. Going to be using this subset of the 2022 season to conduct my tests on. Decided to make it static instead of loading from the NBA api because of the case that the NBA api were to ever close, break, or something unforeseen were to happen. Hopefully these are the only static records I need for the tests because they were a pain the arse to copy and paste to and from.

End: 11pm

# 19/11/22

I've realised that having a 174 static `DataFrame` is not really hopeful. Mainly because then it seems difficult to make modifications and checking those modifications in tests. So, I decided to take an even smaller subset of games. Now, it's only 2 games, or 4 entries, for each game type. Regular, playin, and playoffs makes the `DataFrame` equal to 24 entries. I think this is a really managable size that I can also hard code and check easily with. I've also started thinking about reducing the columns of `Schedule.games`. Mainly because having that many extra columns for a pretty large `DataFrame`, I think, seems like I'm adding unnecessary time added to run my program. I left all those extra stat columns in originally because I thought I would need them later on in other iterations, probably still do, but for the time being, it's just bloat. Besides, it wouldn't be too difficult to add them back anyways because I'm actually adding code to delete them in the first place, so it would easy to revert back. I removed all the unnecessary columns and now it looks like this:

```
Schedule.games.columns = [
  'GAME_NUM',
  'TEAM_ABBREVIATION',
  'TEAM_NAME',
  'GAME_ID',
  'MATCHUP',
  'WL',
  'PLUS_MINUS',
  'GAME_TYPE',
  'LOCATION'
]
```

I added a new python file to hold the static data that my tests can call on to get. The new file is `static_game_logs.py`.

I just found a case that needs to be accounted for when creating schedules. A game that is currently live is returned by `leaguegamelog`. Though the fix is easy enough with the fact the the `WL` column remains empty til the game is completed and updated.

Noticed that my `test_game_logs` don't include `GAME_NUM` as the index. To further make the problem a bit more annoying, `GAME_NUM` is the accumulation of the regular season to the playoffs. So, to get the correct `GAME_NUM`, I'll have to call `leaguegamelog` again and get all the games and calculate the `GAME_NUM`. But I'll do that some other time.

# 23/11/22

Start: 8:30pm

Removed uneccessary code from `elo_system.py`.

Revisited some coding concepts related to OOP. I've realised that my code has low cohesion because some, if not all, of my classes have methods not relating to the class. Going to have to refactor more code later.

End: 9:15

# 27/11/22

Start: 5:00pm

I wrote test cases for `SeasonSchedule.initialise` and I think they're all that's needed. I could write more relating to the data but since I use `leaguegamelog` to get the data and I only trim them. I don't think I need to write cases for the data since it is an outside source. Also, I've realised that I can modify `SeasonSchedule.initialise` function parameters to take in a `DataFrame` instead of a `year: String` so that it's easier to test because I'm not calling `leaguegamelog`. That means I can use a subset of games to call `SeasonSchedule.initialise` with so that testing times are shorter.

So anyways, I only wrote a test case concerning:
- The columns. Since I trim and add new columns.
- Data in the index column. Since I create and use that as the index.
- Data in the game type column. Again, since I create the column and populate it.
- Finally, data in the location column. Again, same thing as above.

I found two bugs in my code just from these four tests. They were easily fixed though.

Moved a few functions around to different class to improve cohesion, I think. And with that, I have my second iteration of my class diagram done.

![second class diagram 21_11_22 drawio](https://user-images.githubusercontent.com/117491084/204128074-55b6b1d3-aa16-4e00-a001-95bc67b7fb89.png)

End: 8:00pm

# 29/11/22

I didn't get to write any code but I did do a tiny bit of research.

I had an idea that I should look into .NET. Now, before this I had no idea of what it was. I thought it was a programming language because I would constantly see it listed as a requirement on job posts about the relevant experience needed for software related jobs. After watching a video, found out that it's actually a framework where you can more easily deploy applications because of the inbuilt functionalities. Now, why is this important to my project? I had a thought that I might actually try to implement this current project using the .NET framework. I'm thinking about getting my feet wet with using C# or any other langauge that's needed to develop the web application. I'm going to be giving it a go translating my current python code to C# in the .NET framework once I complete all the tests (complete this iteration). Once I move all the python code to the .NET framework, I'll be assessing how easy it to use the framework because at the end of the day, I don't want to spend too much time wasting away with this. But... at the same time, this might be very beneficial if I am able to learn this. Guess I'll see how it goes. The video I watched showed some C# code and it looks pretty similar to C++ syntax so I hope it's a smooth transition if I do go that route.

Back to tests. I said this yesterday.
> I could write more relating to the data but since I use `leaguegamelog` to get the data and I only trim them. I don't think I need to write cases for the data since it is an outside source.

After thinking about a bit, I'm going to write a test for the `DataFrame` that's returned from using `leaguegamelog`. At first, I just thought about testing the actual data itself for a whole season and thinking how time consuming that would be to copy and paste all that information into `static_game_logs.py`. But in reality, I can just use a single game to do this because it's able to test the format of the columns and the values of the columns so that it's always what I'm expecting.

# 3/12/22

Completed the tests for the `SeasonSchedule` class but I've also made some changes to the class and parent class, `Schedule`.

First, the biggest change I made to `Schedule` was that I changed it to an abstract class. Since python doesn't heavily focus on OOP, I thought that it won't have abstract classes. But, it did. So, I'm able to use `ABC` and `abstractmethod` from the `abc` module to define my abstract classes with to make sure I can't instantiate abstract classes. At first, I didn't have an abstract method in `Schedule` because I saw no need for it since I didn't need it. However, this meant that I was able to do this:
```
from abc import ABC

Schedule(ABC):
  def add_games():
    pass
  
  def get_game():
    pass
  
foo = Schedule()
```
This code will run fine because `ABC` does not define this example `Schedule` class as an abstract class.

According to the [docs](https://docs.python.org/3.9/library/abc.html#abc.abstractmethod):
> A class that has a metaclass derived from ABCMeta cannot be instantiated unless all of its abstract methods and properties are overridden.

As a quick note if there's any confusion about what `ABCMeta` that was just mentioned. `ABC` implicitly defines `ABCMeta` for us and makes code easier to read. From the [docs](https://docs.python.org/3.9/library/abc.html#abc.ABC):

> ```
> from abc import ABCMeta
>
>   class MyABC(metaclass=ABCMeta):
>     pass
> ```

So, back to abstract classes and `Schedule`. I could have no abstract methods and just use `ABC` to signify that it's an abstract class but that bothers me a bit. So, I added the following:
```
import pandas as pd
from abc import ABC, abstractmethod

Schedule(ABC):
  @abstractmethod
  def __init__(self) -> None:
    self.games = pd.Dataframe()

SeasonSchedule(Schedule):
  def __init__(self) -> None:
        super().__init__()
```

Now, when I try to do the following:
```
foo = Schedule()
```

It returns:
```
TypeError: Can't instantiate abstract class Schedule with abstract method __init__
```

Not perfect but the only simple workaround I found. Since I've changed `Schedule`, I'll have to remember to update the class diagram.

Another *major* change, I guess, is that I added a class variable `teams` that keeps track of all current NBA teams. Since both `Season` and `Team` have a list of `self` objects, I've thought about adding an `NBA` class that instead keeps track of all `Season` and `Team` objects but I kinda don't see why I should add extras for no reason when it's still fine to me. So, I've decided not to. Also, added a static method to both `Team` and `Season`. They both just search their respective class variable list for the given variable. For example, getting the `Team` object given a team name or getting the `Season` object given a year. Speaking of the `Season` class, I added a global variable `get_both_games` that decides how `SeasonSchedule.get_team_schedule()` behaves. Before it was:
```
SeasonSchedule(Foo):
  def get_team_schedule(team_abbreviation) -> pd.DataFrame:
    return self.games[self.games.MATCHUP.str.contains(team_abbreviation)]

Season():
  def initialise_team_schedules():
  ...
    season_games = self.schedule.get_team_schedule(team_abbreviation)
  ...
  team.schedule.add_games(season_games)
```
And now:
```
def get_team_schedule(self, team_name) -> pd.DataFrame:
  if get_both_games:
    return self.games[self.games.MATCHUP.str.contains(team_name)]
  else:            
    return self.games[self.games.TEAM_NAME == team_name]

Season():
  def initialise_team_schedules():
  ...
    if get_both_games:
      season_games = self.schedule.get_team_schedule(team.abbreviation)
    else:
      season_games = self.schedule.get_team_schedule(team.name)
  ...
  team.schedule.add_games(season_games)
```
Basically, I can toggle between using the team's abbreviation or the team name. But the biggest difference is that using only the team name means that `Team.schedule` will only contain one entry per `GAME_ID` instead of two. `Team.schedule` will no longer store the oppositions game stats and now will have to use `GAME_ID` to find the oppositions stats from `Sesaon.schedule`. As of right now, `get_both_games = False`.

Finally, did refactor `Elo` a bit by adding a helper function as to not repeat code. Nothing major or even minor really.

I've also completed the tests for `Elo` and something I should *probably* do is add some graphs that visualise some/all of my math functions in `Elo`. I could then easier visualise how the probability of winning changes depending on $\text{RDiff}$, $\text{K}$, and so on. But again, that's just something to do on the side maybe.

Now I only have `Season` to write tests for since `Team` doesn't have anything that I would need to test for.

# 4/12/22

I've realised that I've forgot to explain a slight change to $\text{W}$ that I made while coding.

This was what I thought $\text{W}$ should be set to before I started coding:

>$$ 
\text{W} =
  \begin{cases}
    \displaystyle 1 & \quad \text{a win} \\
    \displaystyle 0.5 & \quad \text{goes OT} \\
    \displaystyle 0 & \quad \text{a loss}
  \end{cases}
$$

I removed the overtime value for simplicity. So, $\text{W}$ is now:

$$ 
\text{W} =
  \begin{cases}
    \displaystyle 1 & \quad \text{a win} \\
    \displaystyle 0 & \quad \text{a loss}
  \end{cases}
$$

Now, to $\text{W}_{e}$. $\text{W}_e$ is calculated using this formula:

>$$\frac{1}{10^{-\frac{\text{RDiff}+\text{HomeAdv}}{x}}+1}$$

But for simplicity, $\text{RDiff} = \text{RDiff} + \text{HomeAdv}$. So,
$$\frac{1}{10^{-\frac{\text{RDiff}}{x}}+1}$$

I made a little video showcasing how $x$ scales $\text{W}_{e}$ below.

https://user-images.githubusercontent.com/117491084/205468009-e5710d44-6381-4915-8337-6fc2d5f494bd.mp4

We see that setting $x = 200$ is too aggressive while $x = 600$ is not aggressive enough. So I do think that having $x = 400$ is probably the right value. Not because it seems like every other major site that has implemented the Elo system uses $400$.

Also, I've found [fivethiryeight's](https://fivethirtyeight.com/features/how-we-calculate-nba-elo-ratings/) way of calculating the point spread based on Elo.

>Here’s the formula: Take the difference of the two teams’ Elo ratings, add 100 points for the home team and then divide by 28.

This is something that I'm going to want to use for functions I have in mind down the line.

Looks like I haven't explained what $\text{MOV}$ is either. Basically it's a multiplier for the margin of victory which is applied to both calculating the winning and losing team's Elo's. So $\text{MOV}$ is calculated from the winning team's side $(\text{Win}_{team})$. The formula is:

$$
\text{MOV} = \frac{(\text{Win}_{team}\text{Margin} + 3)^{0.8}}{7.5 + 0.006 \times (\text{Win}_{team}\text{R}_{o} - \text{Lose}_{team}\text{R}_{o} + \text{Win}_{team}\text{HomeAdv})}
$$

We can see how $\text{MOV}$ is used here:
>$$\text{R}_n=\text{R}_o+\text{K}\times\text{MOV}\times\left(\text{W}-\frac{1}{10^{-\frac{\text{RDiff}+\text{HomeAdv}}{x}}+1}\right)$$

So, $\text{Win}_{team}$ and $\text{Lose}_{team}$ both use the $\text{MOV}$ value in their calculations.

Also forgot to mention the change I made to $\text{HomeAdv}$. It is now,

$$ 
\text{HomeAdv} =
  \begin{cases}
    \displaystyle 100 & \quad \text{home game} \\
    \displaystyle -100 & \quad \text{away game}
  \end{cases}
$$

Something that I got confused about is that when calculating $\text{MOV}$, I have to calculate `RDiff` of the winner. If I had explained earlier what $\text{MOV}$ is, this probably wouldn't have happened. I got pretty confused why `Elo.calculate_elo()` wasn't working but it was I was using the losers `Elo.margin_of_victory()` method to calculate $\text{MOV}$. Because of this confusion, I've decided to change the signature of `Elo.margin_of_victory()`. It was:
```
def margin_of_victory(self, margin, OPPRo, location):
  return ((margin + 3)**0.8) / (7.5 + 0.006 * (self.elo - OPPRo + (self.home_adv_calc(location)*self.home_adv)))
```
To:
```
@staticmethod
def margin_of_victory(margin, RDiff, location):
  return ((margin + 3)**0.8) / (7.5 + 0.006 * (RDiff + Elo.home_adv_calc(location)*Elo.home_adv))
```
Now it doesn't have to depend on `Elo.elo` anymore and I can just use either class to calculate $\text{MOV}$.

Something I just thought of, which is crazy considering, is why I don't just calculate the change in Elo for the winning team and then just minus the value for the losing team. I will see how this goes.

Now onto the changes I made to my classes.

First, I changed the `Schedule` by removing the abstract method tag on `__init__()` because now, `add_games(games)` is an abstract method. I made it an abstract method after I realised that the change I made yesterday meant that what was originally coded didn't make sense for both subclasses.
> But the biggest difference is that using only the team name means that `Team.schedule` will only contain one entry per `GAME_ID` instead of two. `Team.schedule` will no longer store the oppositions game stats and now will have to use `GAME_ID` to find the oppositions stats from `Sesaon.schedule`.

This meant that `TeamSchedule.add_games()` and `SeasonSchedule.add_games()` acted similarly, but not the same. Which is good news because having `__init__()` as an abstract method was a little bit silly.

The biggest changes I made were to the `Elo` class. All the calculating methods besides `carry_over()` now return a value and are static methods. I also added a new function, `calculate_elo_change()` that returns the change in Elo rating. This is useful because now, I don't have to call `calculate_elo()` twice for each game. I can just calculate the change and negate the value to get the other teams change in Elo rating. So, then I had to add getter's, setter's and `update_elo()` for `Elo.elo` to accomodate these changes. `carry_over()` doesn't need to be a static method because I don't see why I would need to calculate the carry over because it's only called at the end of the season. Calculating the carry over at the end season without another season schedule would be pointless I think. Adding in these static methods meant I had to change the behaviour of `Season.initialise_team_elos()` a bit and of course the testing suite.

Finally, I've completed the tests for `Season` and that concludes the testing suite for this iteration. My next aim is probably to try and convert my current code into the .NET framework and see how that goes. I can finally push simple-backend branch into main now.

# 5/12/22

I've restructured my project files into a more proper arrangement. Added a bit to the [readme](../README.md) file. Created a [Elo rating explanation](elo_rating_formula.md) file that contains the formula used and an explanation for them. It isn't as comprehensive as the explantions here though, but it's enough for anyone to understand... I hope.

I know that this problem isn't really relevant, yet, to my app but I'm thinking about how the nba-api is quite restrictive in how many calls I can make before it stops responding. I've experienced being blocked after four calls to the api so I'm trying to think of a way to prevent this ever being a problem because the only way I could think about fixing it was with `sleep()`. However, that slowed down the program significantly and I don't want to use that. I'm thinking of maybe adding a database(db) to my project and some how being able to get all the data, i.e. all sesaon game logs from the earliest season to the latest. Then, by storing the data in a db, I don't have to make calls to `leaguegamelog` anymore and risk being temporarily be blocked.

[Sports-reference](https://www.sports-reference.com/) does allow [web scrapping but only at 20 requests per minute](https://www.sports-reference.com/bot-traffic.html). But, unfortunately, it doesn't allow you to use their complied data.

Found the ESPN-api again. It's weird how there's no official documentation for the api. The documentation for their api was last updated around 2014 it seems based on the fact that a post about not giving public api keys anymore was posted in 2014 and it says it was only 'posted 4 months ago'. Nevertheless, I found [unofficial documentation](https://github.com/ianpherbert/ESPN-API-Documentation) for the NFL and a less comprehensive documentation in terms of the number of endpoints covered for a sport, [here](https://gist.github.com/akeaswaran/b48b02f1c94f873c6655e7129910fc3b). The second one is great because there is a pretty active comment chain where people can get answers about the api. The ESPN hidden API Docs shows a wider range of endpoints(more sports), but the NFL documentation is more detailed. I've tried the NFL documentation and it works for the NBA too. Just have to convert 'football' to 'basketball' and 'nfl' to 'nba'. So far, I've been able to get every NBA team and call the api for each nba team. There seems to be no limit to the number of calls to the api which is great. Again, there still probably is, I just haven't reached it yet. So that's good news. Also, I was able to find an endpoint that returns the season schedule for a team.

I'm not going to bother with changing api's til I complete the front and can use a basic version of the app. So, this is as far as I'll take this, for now.

# 6/12/22

After about a few hours of looking into .NET and what framework to actually use - like ASP.NET, I decided to put this off until I complete the front end with what will probably be with flask. I'll leave the .NET development branch up for later use.

# 9/12/22

Created a new branch for the front end of the first iteration. Now, will just need to decide whether I use Django or Flask.

I've decided on Flask and created some tasks to reflect what the frontend should be by the end of the iteration.

I added some folders and files to structure my project like a flask project. I completed the `base.html` file that displays what every page should have for it's header/footer/format. So, for the time being, my base html file is completed barring any issues that I have with the layout when displaying all teams in a table.

# 10/12/22

Found an a bug in `elo_system.py`. The attribute `TEAM_NAME` from using `leaguegamelog` is not *always* the same as the `FULL_TEAM_NAME` in `nba_api.stats.static.teams`. So, that means I have to use something else to match game to team. It's now using `TEAM_ABBREVIATION` to do this instead. I will need to update the testing to reflect this change. Wanted to keep all backend modifications to it's own branch but unfortunately, didn't.

Didn't mention this yesterday but the header of the website contains `Teams` and `About` which are just placeholders that do nothing at the moment. `Home` does redirect the user to the main page.

Made some changes to the `index.html` and `base.html`. Some minor formatting changes and the same with `style.css`. I created a `models.py` file where it instantiates classes from `elo_system.py`. It isn't ideal but I'll leave it for now.

Completed the first iteration of the frontend which is great. Now, before I move on to new features. I'm going to try and solve this problem,

> I've experienced being blocked after four calls to the api so I'm trying to think of a way to prevent this ever being a problem because the only way I could think about fixing it was with `sleep()`.

This problem isn't an issue at the moment, but in the future, if I want to calculate historical data, then there'll be too many calls to NBA-api. To fix this, I'm thinking of setting up a database in MySQL which is a simple lightweight database. With this database, I would have to initialise it if it didn't exist already. To initialise the database, I would need data. The data I would currently need would only be the 22' and 23' seasons which is what I already have, just not in database form. But, as I said earlier, that wouldn't work with how I get my data at the moment.

To try and solve this, I have two ideas:
1. Use the ESPN-api to gather the data. Since there's seemingly no limit to the number of calls to the api, I won't have a problem because from the documentation that I've gathered earlier, there are no calls to get whole seasons worth of game logs. So, I'll have to combine data across different calls.
2. Use the NBA-api to gather the data but use `sleep()`. Hopefully it doesn't come to this solution since the performance is poor.

# 11/12/22

Now that I've completed the first iteration, I'm just going to make a front end and a back end branch where I'll be making changes to both on a rolling basis. Instead of having iteration branches, I'm just going to be using these branches to implement/fix features because I have no real end goal and can constantly come up with new features. As an aside, backend and server mean the same thing in the context of the web application.

The next milestone of the project is to implement the database.

I decided on MySQL earlier but I really don't need a fully fledged dbms. So, I'll be using pythons SQLite for my database.

# 13/12/22

Making decent progress on retrieving data from ESPN's api. Will write about it tomorrow.

# 14/12/22

I'm able to use the ESPN api to retrieve a whole sesaon's worth of data and formatted it to match my relational diagram. Speaking of diagrams, here is my ERD and RD for my database.
  
![entity relationship diagram](https://user-images.githubusercontent.com/117491084/207506817-5fc088ce-96c1-4da1-b3a4-336f17dcff27.png)
  
![relational diagram](https://user-images.githubusercontent.com/117491084/207506841-f05d718a-d356-454c-b0ba-8c0831d35837.png)

Now, the next step is to set up the database and insert the values.

I found a few problems with ESPNs api, or at least, problems when it comes to older historical data. First of all, it seems like the limit on how far you can gather data is back to the 2003 season. Not sure if this is correct but it seems they store 20 nba seasons of data. So, with that being said, I won't be able to get older data unfortunately. Will have to use another source for that when once I implement functionality for historical seasons. Another potential problem is that the the number of teams throughout the seasons change. Another quirk that I'll have to look out for is that team names change and the team endpoint for ESPN, doesn't return historical teams either, only current teams. For now, I can create the nba season from 2005 onwards so that 2004 and 2003 are unable to work with this current iteration because there is one less team in nba.

Created an [ideas file](ideas.md) to contain ideas I have about the functionality or ui of the web app.

Completed loading data into the database. Now when running `db.py`, seasons 2005-2023 will be stored in database.

The next thing to do is to update the classes in `elo_system`. Since there is no more data to manage anymore, I will probably change most, if not all, methods that aren't redundant to static.

# 15/12/22

After some more thinking and research, it's best if I just use sqlalchemy to manage the database. This change means that `elo_system.py` is now depreciated. I'll probably keep it around because I still might use the NBA-api to get historical data since I can't with ESPN's.

# 20/12/22

Finally, after some time I've modified `db.py` to initialise team elo's using data from the 05' season all the way to the current date. Along the way, I found a bug. Let's go through it.

One bug that I've found had to do with my first iteration. The first iteration used `NBA-api` to get data and I found that there was a problem with `GAME_ID`. The problem is that when a game is scheduled, `GAME_ID` is created. So, if a game were to be postponed, that would mean the game being played at a later date. Since the `gamelogs` were sorted by `GAME_ID`, the elo calculation would be too soon and not reflective of what their recent elo rating is. So, to fix this, I sorted by date when selecting the season games from the `plays_in` table. To sort by date, I modified my `game` table schema to include a date column.

This is also the reason - probably - why I found another inconsistency. When calculating the elo of teams from the 22' season, using the first iteration system gave a different elo rating for teams than the new system. Again, due to how the games were sorted in the first iteration, it would not calculate the updated elo rating at the correct time which meant a cascade of differences between the two systems.

Updating the front-end was simple and I found no problems at all.

Finally, I've renamed `elo_system.py` to `elo_calculator.py`. Removed all classes from `elo_calculator.py` except for `Elo` which is now renamed as `EloCalculator`. Deciding to keep it as a class instead because there are variables that make more sense to access from a class than from an import... I think.

The time it takes to run `db.py` the first time is about 9 minutes, which is quite a while. Subsequent run times are about 6 minutes. Also, weirdly enough, `team.elo` is a float when queried from the front end. I've fixed it in jinja by just type casting `team.elo` to `int` but it's weird. Not sure why the database contraints aren't working or even the model contstraints. I fixed this by type casting `elo` in the `DataFrame` of the season games in `db.py`. Turns out it's because `round()` returns a `float` type.

The last step before pushing to main, is to update the database with only new games that have an outcome. I was able to get the code done for updating the table up til the current date. Just hasn't been tested yet...

# 21/12/22

Updating the database seems to be working as expected. I decided not to use a `DataFrame` but just a list of dicts because it's much less memory bloating for something simple. I also found a weird bug that when I casted `row['status']` from `iterrows()`, it would change the date somehow even though it was set several lines before. That would result in fetching more games in the return json. Really weird behaviour and I'm not sure why it happened.

But anyways, last, last thing before I push to main, is to figure out if there is a way to call `db.py` to update everytime the web app is started.

So, I've completed that, but I just realised that I need to update the elo's too... and doing so seems like a much bigger task. I think that I should add a flag variable named `is_calculation_required` to the game table. Now, I can have a seperate function for calculating elo's and don't have to rely on `pandas` to help with the calculation anymore. But, I probably won't change it til later.

Added `calculate_elos()` to `db.py` that calculates the new elo rating for the given `game_ids`. Also, from the `run.py` file, it is able to both create and update the db. Now I only have to run `run.py`. The `db.py` file also contains a little work around to an annoying problem. So, if I run `run.py`, I have to use
```
from nba_elo_system.elo_calculator import EloCalculator
```
to import that class. Whereas when I run `db.py`, I have to use
```
from elo_calculator import EloCalculator
```
to import. So, what I've done is add this
```
if __name__ == '__main__':
    from elo_calculator import EloCalculator
    
else:
    from nba_elo_system.elo_calculator import EloCalculator
```
to the top of the file. I've removed this from the version that is pushed to the main branch though. It is only going to be used when debugging and testing needs to be done. Also, I have a global variable `force_init` for debugging and testing too. Basically, when set to true, when I run `db.py`, it will always run `initialise_db()` whereas when it's false, it will always run `update_db()`. I also deleted 'main' because `db.py` is not supposed to be run. Again, it is kept in the database branch version for testing/debugging.

# 23/12/22

There were a few bugs in `calculate_elos()`. One of the noteworthy ones were that having two open connections to the database meant that using the second connection would result in the database getting locked. Also, that I couldn't use the attribute `rowcount` to get the number of returned rows from an `execute()` call. So, that's something to keep in mind for the future. And lastly, if the db partially updates elo ratings, then to fix the problem, I would need to reset team's elo to calculate the elo from the very first game. In saying that, I could write a function that calculates the elo's of given teams, for given play_in tuples. That would mean that I could calculate future games without actually updating the db. Something to think about for future features.

# 24/12/22

Created a new branch to start a working on a new function. `change-in-elo` is a branch where I'll be working on showing to the user the change in a team's elo since the last time the db has been updated. This means that it will only display the change if `update_db()` is run at the start of the web app.

Going to modify the time length of change a bit. Instead of using the last time the db was updated to get the change in elo, I'm thinking of using at least 2, maybe 3, time lengths. First, would be the change from the past game. Second, would be change from a week ago. A game from at least week ago means 7 days ago, which includes that whole day, to the closest game. And lastly, would be the change from a month ago. If there are no games from a specific range, then use the longest range it can. This makes more sense than what I had before because if I updated the db, stopped the app, ran the app again, there would be no change in elo. That would seem a bit silly. Also, with this, you would be able to see if the spikes in a team's elo is random or a trend. So, to do this, I'm going to add 3 new columns to the `team` table for the change in elo to be stored in. This would mean, in `initialise_db()` and `calculate_elos()`, I would need to calculate the dates of the games and if they need to be added to those columns. I've changed my mind again. Instead of using time as the factor, I'm going to use $x$ number of games instead. Where $x = 1$, for the change in elo from game to game, $x = 9$, for intermediate change in elo, and $x = 27$, for the long term change in elo. Kinda decided on $9$ and $27$ because $9$ is a factor of $27$. With this way, I can directly compare the changes in elo since using dates might mean that some team's have more games than others. It's also easier to implement it this way.

Another thing on the to do list is to refactor my `db.py` code. One thing to decide is whether using `Dataframes` is better than a `list(dict())`.

# 1/1/23

Enough of the holiday I guess. To update the 'game change', 'week change', and 'month change' I think I have to update the `games_played` column first then check what updates to 'change' needs to be made.

I found a little bug in calculating the change and I fixed it. Renamed the columns on the webpage to better suit what the column represents.

# 2/1/23

I've removed the `change_in_elo` columns from the table `team`. Now, when calculating the change in elo over $n$ number of games, I've decided to store the change in elo in the `plays_in` table under `elo-change` column. I only have to sum the `elo_change` column for $n$ number of games to get the my result. I've added those changes and it's working as expected, so far...

I've also implemented table sorting using the jQuery plug-in, DataTables. Ran into a few problems but they minor and I was able to solve them relatively quick. As a result of using DataTables, I've created a javascript folder in [/static](../nba_elo_system/static/js/) for my javascript files. `index.js` only contains the datatable set-up and nothing more at the moment. As of right now, I'm able to sort the table using any of the columns and there is an icon displaying how the table is currently sorted for both descending and ascending order. Also a nice little addition, a team search function.

I've ran the branch with all years and it seems to be working fine. Pushed the `change-in-elo` branch to main.

# 3/1/23

Cleaned up `db.py` a bit.

Started new feature of website. Display the up-coming schedule (1 week). I'm able to gather the next week schedule with each game having 2 entries, one for home and away. Each entry has a `PlaysIn` and `Team` object. Just need to decide how I should display the schedule.

# 4/1/23

I got the new `schedule` page up and running. Currently it displays the next week's game schedule. In each game, it contains: the teams playing; home/away; win probability; and projected point differential. I'm just printing it to the page at the moment so I'll have to make it more aestheticly pleasing later. Going to try and pass to the template, rows - a list in python - where they are lengths of 3. That way in the html file `schedule`, I can create 3 horizontal tables to take up the width of the page. Also added a few classes to `style.css` to accomodate `schedule.html`. 

I added a new static method to `EloCalculator`, `projected_point_diff()` to calculate the projected point differential of two given Elo's, as mentioned earlier. Although calculating the projected point differential has nothing to do with the `EloCalculator` class, I added it there anyways because I didn't want to create a new class just to accomodate the one function.

# 10/1/23

I've now completed the `schedule` page up to my standards. I've done quite a bit since the last time so I'm going to go through the changes.

Made a little change to the overall website. I've changed `background-primary` in `style.css`, to a lighter shade of grey because I find it easier to read and it looks better.

I modified the `week_schedule` to be:
```
week_schedule = [
  {
    'day' = str(),
    'date' = date(),
    'games' = [
      [
        {
          'home' = Team()
          'away' = Team()
        }
      ]
    ]
  }
]
```

`week_schedule['games']` is a list of lists where each list is of max length, 2. This is so that I can display each list in the same row on the `schedule` page. `week_schedule` is then sorted by the date. This way I can show the games in order of the date. To help me with this, I created a new file, `nba_elo_system/utils.py` to contain helper functions. I created `add_game_to_day` to put the given game to the correct games list. Finally, I pass `week_schedule` to the `render_template` function. I updated `schedule.html` and `style.css` to accomodate these changes. I also created a new file, `static/js/schedule.js`. This file helps me to colour the teams who are projected to win and lose with green and red respectively. Not only does it colour the teams, but it also calculates the shade of the colour based on the win/loss percentage. I got the `RGB_Linear_Shade` function from this [stackoverflow answer](https://stackoverflow.com/questions/5560248/programmatically-lighten-or-darken-a-hex-color-or-rgb-and-blend-colors/13542669#13542669). This function takes a percentage and rgb colour, and returns a shade of that colour, where 0 is no shade and 1 is the lightest shade (i.e. white).

I've pushed the changes into main.

# 20/1/23

I found a bug in `db.py` where `create_nba_season_data()` is defined. After comparing my own `Schedule` page I found that it was inconsistant with the NBA's upcoming schedule. Games that were played in the very early morning (AEDT) were dated to the previous day for some reason. It was relatively easy to find the fix. It was because the date that was extracted from the ESPN api would be in the GMT time zone. So, to fix the bug, all I had to do was convert to my local time zone, AEDT. Since I am using `astimezone()` with no parameters, it converts the `DateTime` object to local date, time, and time zone so there shouldn't be a problem when AEST becomes the time zone.

I have pushed the fix into main.

In `db.py`, `update_db()` currently only updates games from the same day after 6pm. I've changed it to update even the same day games as they are completed according to the ESPN api, where the `game['status']` would have to equal `3`. Now I don't have to wait til 6pm to see the updates in elo after a game.

I've pushed the changes into main.

# 21/1/23

I've found another bug. This time in `routes.py::schedule()`. Because I've changed `db.py::update_db()` to update elo's as the games for the current day are finished, the current day games on the `Schedule` page are also being affected. This is because when I got to the `Schedule` page, the win probability and projected point differential is calculated with the current Elo value. So, the win probability and projected point differential for a game before it is played to after, are different. This is an inconsistancy that I don't want in the system and so, to fix this, I've decided change the way I get the upcoming schedule. Currently, I would get the current schedule by filtering the `PlaysIn` table with getting a weeks worth of games. The dates would be a week, and would include the current day if it was before 6pm which is *usually* the time the last game would end before. Now, I've modified it to filter the `Game` table instead. This way I can do the same thing but also add the extra check for `Game.status`. As a result, I can only get games that are not completed.

Another change I've made is that I've decided to run `db.py::update_db()` in both `routes.py::index()` and `routes.py::schedule()`. This way, the database can be updated without restarting the app. To do this, I had to modify `__init__.py`, `run.py`, and `routes.py`.

I've pushed the changes into main.

Found another bug. In `db.py::get_updated_games()`, the ESPN api uses dates in the EST format, whereas my database uses my local time zone (AEDT). So, I had to convert the dates to EST to get the correct dates.

I've modified `routes.py::schedule()` to remove days where there are no games and pushed the changes into main.