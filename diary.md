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

Not sure why I went on a Memphis rant - IYKYK. Now, returning to my original point, I think that a team beating seven opponents in a row by a point differential of 10 is more impressive than winning by 70 for a single game. I think that consistancy means more for how good a team is rather than these anomalies. Not sure yet to how I could reward teams with a high point differential but it's something to think about in the future. Also, I should probably add a cap to the point of how much the point differential will affect $\text{K}$. Thinking of something around 20.

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
