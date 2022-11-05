# NBA Power Rankings

Creating my own NBA power rankings system taking inspiration from an [NRL](https://fanalytics.weebly.com/) and [Football](http://www.eloratings.net/) power ranking system. My own and both of these systems are based on Arpad Elo's Elo ranking system used to rate chess players.

The Elo ranking system is based on the following formula:

$$\text{R}_n = \text{R}_o + \text{K} \times (\text{W} - \text{W}_e)$$

The following is my little diary containing thoughts and processes during development. Some terms to be aware of:
|Term|Meaning|
|---|---|
|PR|Power Ranking|
|OT|Over Time|


## 5/11/22

### Formula Explanation

Trying to come up with a modified version of the Elo ranking system based on the NRL and Football power rankings.

Starting from here:
> $$\text{R}_n = \text{R}_o + \text{K} \times (\text{W} - \text{W}_e)$$

$\text{R}_n =$ New PR

$\text{R}_o =$ Pre Match PR

$\text{K} =$ Variable

$\text{W} =$ Result of Game

$\text{W}_e =$ Expected Result

To further clarify some of the independant variables.

#### K

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

#### W

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



#### W<sub>e

$\text{W}_e$ is calculated using this formula:

$$\frac{1}{10^{-\frac{\text{RDiff}+\text{HomeAdv}}{x}}+1}$$

Where $\text{RDiff}$ is the difference in PR. The expected result is always $\geq 0 \text{ and} \leq 1$. This is because even though there is a 100+/- difference in PR, a team is **never** guaranteed a win/loss.

$\text{HomeAdv}$ is a constant. After reading a [post](https://bleacherreport.com/articles/1520496-how-important-is-home-court-advantage-in-the-nba#:~:text=Of%20the%20four%20major%20American,games%20in%20their%20home%20arenas.), I've decided to make home court advantage worth 10%. The article mentions that there is a discrepency between the regular season and playoffs home court advantages. ~61% of home teams in the regular season win, while ~65% of home playoff teams win. The article does say that teams that home teams in the playoffs are always the higher seed so there is that to take into consideration. So, that's why I decided to make home teams 10% better, thus making $\text{HomeAdv}=\text{R}_\text{o}\times0.1$. Although, this does introduce the fact that higher PR teams will gain more from home court. However, it does make sense to me that better teams gain more from home court.

Finally, here is what the full formula looks like:

$$\text{R}_n=\text{R}_\text{o}+\text{K}\times(\text{W}-\frac{1}{10^{-\frac{\text{RDiff}+(\text{R}_\text{o}\times0.1)}{x}}+1})$$

Next, is figuring out what programming language to use. It'll be easier for me to tweak and test the formula once it's been coded than using pen and paper to check.


