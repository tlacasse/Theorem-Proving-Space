CREATE TABLE ConjectureDependency (
    Id           INTEGER PRIMARY KEY ON CONFLICT FAIL AUTOINCREMENT,
    ConjectureId INTEGER REFERENCES Conjecture (Id),
    DependencyId INTEGER REFERENCES Dependency (Id) 
);
