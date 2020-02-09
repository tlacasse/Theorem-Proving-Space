CREATE TABLE Step (
    Id          INTEGER        PRIMARY KEY ON CONFLICT FAIL AUTOINCREMENT,
    TheoremId   INTEGER        REFERENCES Theorem (Id),
    Text        VARCHAR (1000),
    IsProofStep BOOLEAN
);
