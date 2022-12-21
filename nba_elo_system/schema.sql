DROP TABLE IF EXISTS season;
DROP TABLE IF EXISTS game;
DROP TABLE IF EXISTS plays_in;
DROP TABLE IF EXISTS team;

CREATE TABLE season (
    year INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE game (
    id INTEGER PRIMARY KEY,
    season_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    status INTEGER NOT NULL,
    date DATE NOT NULL,
    is_calculation_required BOOLEAN NOT NULL CHECK (is_calculation_required IN (0, 1)),
    FOREIGN KEY (season_id) REFERENCES season (year)
);

CREATE TABLE plays_in (
    game_id INTEGER,
    team_id INTEGER,
    score INTEGER NOT NULL,
    location TEXT NOT NULL,
    outcome TEXT,
    PRIMARY KEY (game_id, team_id)
);

CREATE TABLE team (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    short_name TEXT NOT NULL,
    abbreviation TEXT NOT NULL,
    elo INTEGER NOT NULL
);
