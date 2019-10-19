CREATE TABLE Step (
    Id           INTEGER PRIMARY KEY ON CONFLICT FAIL AUTOINCREMENT,
    ConjectureId INTEGER REFERENCES Conjecture (Id),
    IsUseful     BOOLEAN,
    Text         VARCHAR,
    Tokens       VARCHAR
);
