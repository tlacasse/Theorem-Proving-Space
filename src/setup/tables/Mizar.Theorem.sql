CREATE TABLE Theorem (
    Id        INTEGER        PRIMARY KEY ON CONFLICT FAIL AUTOINCREMENT,
    ArticleId INTEGER        REFERENCES Article (Id),
    Type      VARCHAR (30),
    Header    VARCHAR (1000),
    Statement VARCHAR (1000),
    HasProof  BOOLEAN
);
