from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '691ca0a5f74f0ef59a7054473c6861a333b4df381ee0b774db053d598ca4075b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nba.db'
db = SQLAlchemy(app)

from nba_elo_system import routes