class EloCalculator():
    home_adv = 100
    x = 400
    elo_avg = 1500
    k = 20

    @staticmethod
    def win_expectancy(Ro: int, OPPRo: int, location: str) -> int:
        return 1 / (10**(-((Ro - OPPRo) + (EloCalculator.home_adv_calc(location)*EloCalculator.home_adv)) / EloCalculator.x) + 1)

    @staticmethod
    def w(outcome):
        return 1 if outcome == 'W' else 0

    @staticmethod
    def elo_change(Ro: int, outcome: str, OPPRo: int, location: str, mov:int):
        return  round(
                    EloCalculator.k * 
                    mov * 
                    (EloCalculator.w(outcome) - EloCalculator.win_expectancy(Ro, OPPRo, location))
                    )
    
    @staticmethod
    def elo(Ro: int, outcome: str, OPPRo: int, location: str, mov:int):
        return Ro + EloCalculator.elo_change(Ro, outcome, OPPRo, location, mov)

    @staticmethod
    def margin_of_victory(margin, RDiff, location):
        return ((margin + 3)**0.8) / (7.5 + 0.006 * (RDiff + EloCalculator.home_adv_calc(location)*EloCalculator.home_adv))

    @staticmethod
    def home_adv_calc(location: str) -> int:
        return 1 if location == 'home' else -1