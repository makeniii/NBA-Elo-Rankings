# NBA Power Rankings

Creating my own NBA power rankings system taking inspiration from an [NRL](https://fanalytics.weebly.com/) and [Football](http://www.eloratings.net/) power ranking system. My own and both of these systems are based on Arpad Elo's Elo ranking system used to rate chess players.

The Elo ranking system is based on the following formula:

**Rn = Ro + K × (W - We)**

The following is my little diary containing thoughts and processes during development. Some terms to be aware of:
|Term|Meaning|
|---|---|
|PR|Power Ranking|
|OT|Over Time|


## 5/11/22

Trying to come up with a modified version of the Elo ranking system based on the NRL and Football power rankings.

Starting from here:
> **Rn = Ro + K × (W - We)**

**R<sub>n</sub>** = New PR

**R<sub>o</sub>** = Pre Match PR

K = Variable

W = Result of Game

We = Expected Result

To further clarify some of the independant variables.

###### K

There two factors to take into consideration for calculating K:
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

As for score difference, deciding to have it not affect K as of now. Just to make starting easier.

###### W

I tried to have W set according to the following table:

|Time|Win|
|---|---|
|Regulation|1+/-|
|OT|0.65+/-|
|OT2|0.6125+/-|
|OT3|0.575+/-|
|OT4|0.5375+/-|

So for example, if you win during regulation time, W is set to 1 and the losing team will have W set to -1 and so on. But I realised that We could not calculate if a game would go double/triple/quadruple overtime since it only returns a percentage.

So I just set W to:
* 1 for a win
* 0.5 for draw/OT
* 0 for a loss

###### We

We is calculated using this formula:

$$\frac{1}{10^{-\frac{\text{RDiff}+\text{HomeAdv}}{x}}+1}$$

Where $\text{RDiff}$ is the difference in PR. The expected result is always $\geq 0 \text{ and} \leq 1$. This is because even though there is a 100+/- difference in PR, a team is **never** guaranteed a win/loss.

$\text{HomeAdv}$ is a constant. After reading a [post](https://bleacherreport.com/articles/1520496-how-important-is-home-court-advantage-in-the-nba#:~:text=Of%20the%20four%20major%20American,games%20in%20their%20home%20arenas.), I've decided to make home court advantage worth 10%. The article mentions that there is a discrepency between the regular season and playoffs home court advantages. ~61% of home teams in the regular season win, while ~65% of home playoff teams win. The article does say that teams that home teams in the playoffs are always the higher seed so there is that to take into consideration. So, that's why I decided to make home teams 10% better, thus making $\text{HomeAdv}=\text{R}_o\times0.1$. Although, this does introduce the fact that higher PR teams will gain more from home court. However, it does make sense to me that better teams gain more from home court.

Finally, here is what the full formula looks like:

$$\text{R}_n=\text{R}_o+\text{K}\times(\text{W}-\frac{1}{10^{-\frac{\text{RDiff}+(\text{R}_o\times0.1)}{x}}+1})$$

Next, is figuring out what programming language to use. It'll be easier for me to tweak and test the formula once it's been coded than using pen and paper to check.

