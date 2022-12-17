from nba_elo_system import db


class Season(db.Model):
    Year = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(7), unique=True, nullable=False)
    Games = db.relationship('Game', backref='Season', lazy=True)

    def __repr__(self):
        return f"Season('{self.Year}', '{self.Name}')"


class Game(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    SeasonID = db.Column(db.Integer, db.ForeignKey('Season.Year'), nullable=False)
    Type = db.Column(db.String(15), nullable=False)
    Status = db.Column(db.Integer, nullable=False)
    PlaysIns = db.relationship('PlaysIn', backref='Game', lazy=True)

    def __repr__(self) -> str:
        return f"Game('{self.ID}', '{self.SeasonID}', '{self.Type}', '{self.Status}')"


class PlaysIn(db.Model):
    GameID = db.Column(db.Integer, db.ForeignKey('Game.ID'), primary_key=True)
    TeamID = db.Column(db.Integer, db.ForeignKey('Team.ID'), primary_key=True)
    Score = db.Column(db.Integer, nullable=False)
    Location = db.Column(db.String(4), nullable=False)
    Outcome = db.Column(db.String(1), nullable=True)

    def __repr__(self) -> str:
        return f"PlaysIn('{self.GameID}', '{self.TeamID}', '{self.Score}', '{self.Location}', '{self.Outcome}')"


class Team(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.Text, nullable=False)
    ShortName = db.Column(db.Text, nullable=False)
    Abbreviation = db.Column(db.Text, nullable=False)
    Elo = db.Column(db.Integer, nullable=False, )
    PlaysIns = db.relationship('PlaysIn', backref='Team', lazy=True)

    def __repr__(self):
        return f"Team('{self.ID}', '{self.Name}', '{self.ShortName}', '{self.Abbreviation}', '{self.Elo}')"