class Elo_Calculator():
    home_adv = 100
    x = 400
    elo_avg = 1500
    k = 20

    def __init__(self) -> None:
        self.elo = 1500
    
    def __repr__(self) -> str:
        return str(self.elo)

    def carry_over(self):
        self.elo = round((.75 * self.elo) + (.25 * self.elo_avg))

    def set_elo(self, Rn: int) -> None:
        self.elo = Rn

    def get_elo(self) -> int:
        return self.elo
    
    def update_elo(self, total_change: int) -> None:
        self.elo += total_change

    @staticmethod
    def win_expectancy(Ro: int, OPPRo: int, location: str) -> int:
        return 1 / (10**(-((Ro - OPPRo) + (Elo_Calculator.home_adv_calc(location)*Elo_Calculator.home_adv)) / Elo_Calculator.x) + 1)

    @staticmethod
    def w(outcome):
        return 1 if outcome == 'W' else 0

    @staticmethod
    def elo_change(Ro: int, outcome: str, OPPRo: int, location: str, mov:int):
        return  round(
                    Elo_Calculator.k * 
                    mov * 
                    (Elo_Calculator.w(outcome) - Elo_Calculator.win_expectancy(Ro, OPPRo, location))
                    )
    
    @staticmethod
    def elo(Ro: int, outcome: str, OPPRo: int, location: str, mov:int):
        return Ro + Elo_Calculator.elo_change(Ro, outcome, OPPRo, location, mov)

    @staticmethod
    def margin_of_victory(margin, RDiff, location):
        return ((margin + 3)**0.8) / (7.5 + 0.006 * (RDiff + Elo_Calculator.home_adv_calc(location)*Elo_Calculator.home_adv))

    @staticmethod
    def home_adv_calc(location: str) -> int:
        return 1 if location == 'home' else -1