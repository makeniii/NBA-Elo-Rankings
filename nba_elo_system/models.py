from nba_elo_system import db


class Season(db.Model):
    year = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(7), unique=True, nullable=False)
    games = db.relationship('Game', backref='season', lazy=True)

    def __repr__(self):
        return f"Season('{self.year}', '{self.name}')"


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey('season.year'), nullable=False)
    type = db.Column(db.String(15), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    is_calculation_required = db.Column(db.Boolean, nullable=False)

    plays_in = db.relationship('PlaysIn', backref='game', lazy=True)

    def __repr__(self) -> str:
        return f"Game('{self.id}', '{self.season_id}', '{self.type}', '{self.status}', '{self.date}', '{self.is_calculation_required}')"


class PlaysIn(db.Model):
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(4), nullable=False)
    outcome = db.Column(db.String(1), nullable=True)
    elo_change = db.Column(db.Integer, nullable=True)

    game_date = db.deferred(db.select([Game.date]).where(Game.id == game_id).scalar_subquery())

    def __repr__(self) -> str:
        return f"PlaysIn('{self.game_id}', '{self.team_id}', '{self.score}', '{self.location}', '{self.outcome}', '{self.elo_change}')"


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    short_name = db.Column(db.Text, nullable=False)
    abbreviation = db.Column(db.Text, nullable=False)
    elo = db.Column(db.Integer, nullable=False)

    plays_in = db.relationship('PlaysIn', order_by='desc(PlaysIn.game_date)', backref='team', lazy=True)

    def __repr__(self):
        return f"Team('{self.id}', '{self.name}', '{self.short_name}', '{self.abbreviation}', '{self.elo}')"