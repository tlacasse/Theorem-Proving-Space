CREATE TABLE Conjecture (
    Id         INTEGER PRIMARY KEY ON CONFLICT FAIL,
    IsTraining BOOLEAN,
    Name       VARCHAR,
    Text       VARCHAR,
    Tokens     VARCHAR
);
