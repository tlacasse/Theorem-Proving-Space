CREATE TABLE Dependency (
    Id           INTEGER PRIMARY KEY ON CONFLICT FAIL AUTOINCREMENT,
    ConjectureId INTEGER REFERENCES Conjecture (Id),
    Name         VARCHAR,
    Text         VARCHAR,
    Tokens       VARCHAR
);
