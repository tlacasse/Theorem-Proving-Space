CREATE TABLE ConjectureStep (
    Id           INTEGER PRIMARY KEY ON CONFLICT FAIL AUTOINCREMENT,
    ConjectureId INTEGER REFERENCES Conjecture (Id),
    StepId       INTEGER REFERENCES Step (Id),
    IsUseful     BOOLEAN
);
