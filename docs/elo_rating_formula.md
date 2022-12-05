# Elo Rating Formula Explanation

My Elo rating system is based on the following formula:

$$\text{R}_n = \text{R}_o + \text{K} \times \text{MOV} \times (\text{W} - \text{W}_e)$$

## $\text{R}_{n}$
$\text{R}_{n}$ is the new Elo rating, i.e. after the game.

## $\text{R}_{o}$
$\text{R}_{o}$ is the old Elo rating, i.e. before the game.

## $\text{K}$
The $\text{K}$ factor determines how fast the Elo ratings change per game. Currently,
$$\text{K} = 20.$$

## $\text{MOV}$
The **M**argin **O**f **V**ictory variable where the larger the margin of victory, the larger the variable. $\text{MOV}$ is only calculated once from the winning teams side for each game. Currently defined as,
$$
\text{MOV} = \frac{(\text{Margin} + 3)^{0.8}}{7.5 + 0.006 \times (\text{R}_{o} - \text{OPPR}_{o} + \text{HomeAdv})}
$$

Variable|Explanation|
:---:|:---:
$\text{Margin}$|The plus minus of the winning team, i.e. the margin of victory.
$\text{R}_{o}$|The old Elo rating, i.e. before the game.
$\text{OPPR}_{o}$| The opponent's old Elo rating, i.e. before the game.
$\text{K}$|Determines how fast Elo ratings change. $\text{K} = 20$.
$\text{HomeAdv}$| $\text{HomeAdv} = \begin{cases} \displaystyle 100 & \quad \text{home game} \\ \displaystyle -100 & \quad \text{away game} \end{cases}$

## $\text{W}$
$\text{W}$ is the outcome of the match. Currently,
$$
\text{W} = 
    \begin{cases} 
        \displaystyle 1 & \quad \text{win} \\
        \displaystyle 0 & \quad \text{loss}.
    \end{cases}
$$

## $\text{W}_e$
$\text{W}_e$ is the win expectancy or $\text{P}(\text{Win})$. The formula is,

$$\frac{1}{10^{-\frac{\text{R}_{o} - \text{OPPR}_{o}+\text{HomeAdv}}{x}}+1}.$$

Variable|Explanation|
:---:|:---:
$\text{R}_{o}$|The old Elo rating, i.e. before the game.
$\text{OPPR}_{o}$| The opponent's old Elo rating, i.e. before the game.
$\text{HomeAdv}$| $\text{HomeAdv} = \begin{cases} \displaystyle 100 & \quad \text{home game} \\ \displaystyle -100 & \quad \text{away game} \end{cases}$
$x$|Determines how fast win expectancy changes. $x = 400$.

## More infomation

I have more information on the formula and changes that I've went through in my [diary](diary.md) if interested.

