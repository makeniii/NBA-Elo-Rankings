DROP TABLE IF EXISTS Season;
DROP TABLE IF EXISTS Game;
DROP TABLE IF EXISTS PlaysIn;
DROP TABLE IF EXISTS Team;

CREATE TABLE Season (
    Year INTEGER PRIMARY KEY,
    Name TEXT UNIQUE NOT NULL
);

CREATE TABLE Game (
    ID INTEGER PRIMARY KEY,
    SeasonID INTEGER NOT NULL,
    Type TEXT NOT NULL,
    Status INTEGER NOT NULL,
    FOREIGN KEY (SeasonID) REFERENCES Season (Year)
);

CREATE TABLE PlaysIn (
    GameID INTEGER,
    TeamID INTEGER,
    Score INTEGER NOT NULL,
    Location TEXT NOT NULL,
    Outcome TEXT,
    PRIMARY KEY (GameID, TeamID)
);

CREATE TABLE Team (
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    ShortName TEXT NOT NULL,
    Abbreviation TEXT NOT NULL,
    Elo INTEGER NOT NULL DEFAULT 1500
);
