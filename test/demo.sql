CREATE TABLE Team(
    ID int NOT NULL,
    Name varchar(20) NOT NULL,
    Player_ID int(20),
    Company varchar(20),
    Uniform varchar(50),
    NextAgainst int,
    ChallengeTeamID int NOT NULL,
    PRIMARY KEY (ID)

);

CREATE TABLE Stadium(
    ID int NOT NULL,
    Name varchar(20) NOT NULL,
    Address varchar(50),
    Capacity int,
    MotherTeam int,
    Entrance varchar(20),
    PRIMARY KEY (ID)

);

CREATE TABLE Sponsor(
    ID int NOT NULL,
    Name varchar(20) NOT NULL,
    Money int,
    PRIMARY KEY (ID)
);

CREATE TABLE TVcompany(
    ID int NOT NULL,
    Name varchar(20) NOT NULL,
    Anchor varchar(20),
    PRIMARY KEY (ID)
);

CREATE TABLE Vendor(
    StadiumID int NOT NULL,
    Name varchar(20) NOT NULL,
    Goods varchar(20),
    PRIMARY KEY (StadiumID, Name)

);

CREATE TABLE Player(
    Name varchar(20) NOT NULL,
    ID int NOT NULL,
    PRIMARY KEY (ID)

);

CREATE TABLE Season(
    Year int NOT NULL,
    Champion int NOT NULL,
    IsChampionTeamID int NOT NULL,
    PRIMARY KEY (Year)

);

CREATE TABLE Game(
    ID int NOT NULL,
    Date int NOT NULL,
    Away int NOT NULL,
    Home int NOT NULL,
    Address varchar(50) NOT NULL,
    Game_AwayTeamID int NOT NULL,
    Game_HomeTeamID int NOT NULL,
    Game_LocationStadiumID int NOT NULL,
    PRIMARY KEY (ID)

);

CREATE TABLE Statistics(
    ID int NOT NULL,
    Player int NOT NULL,
    Team int NOT NULL,
    Pos varchar(20) NOT NULL,
    AVG float NOT NULL,
    Statistics_PlayerPlayerID int NOT NULL,
    Statistics_TeamTeamID int NOT NULL,
    Statistics_PosStadiumID int NOT NULL,
    PRIMARY KEY (ID)

);

CREATE TABLE FreeAgent(
    Player int NOT NULL,
    FreeAgentPlayerID int NOT NULL,
    PRIMARY KEY (Player)

);

CREATE TABLE Sponse(
    SponsorID int NOT NULL,
    TeamID int NOT NULL,
    PRIMARY KEY (SponsorID, TeamID)

);

ALTER TABLE Team ADD FOREIGN KEY (ChallengeTeamID) REFERENCES Team(ID);

ALTER TABLE Stadium ADD FOREIGN KEY (MotherTeam) REFERENCES Team(ID);

ALTER TABLE Vendor ADD FOREIGN KEY (StadiumID) REFERENCES Stadium(ID);

ALTER TABLE Player ADD FOREIGN KEY (ID) REFERENCES Team(ID);

ALTER TABLE Season ADD FOREIGN KEY (IsChampionTeamID) REFERENCES Team(ID);

ALTER TABLE Game ADD FOREIGN KEY (Game_AwayTeamID) REFERENCES Team(ID);

ALTER TABLE Game ADD FOREIGN KEY (Game_HomeTeamID) REFERENCES Team(ID);

ALTER TABLE Game ADD FOREIGN KEY (Game_LocationStadiumID) REFERENCES Stadium(ID);

ALTER TABLE Statistics ADD FOREIGN KEY (Statistics_PlayerPlayerID) REFERENCES Player(ID);

ALTER TABLE Statistics ADD FOREIGN KEY (Statistics_TeamTeamID) REFERENCES Team(ID);

ALTER TABLE Statistics ADD FOREIGN KEY (Statistics_PosStadiumID) REFERENCES Stadium(ID);

ALTER TABLE FreeAgent ADD FOREIGN KEY (FreeAgentPlayerID) REFERENCES Player(ID);

ALTER TABLE Sponse ADD FOREIGN KEY (SponsorID) REFERENCES Team(ID);

ALTER TABLE Sponse ADD FOREIGN KEY (TeamID) REFERENCES Sponsor(ID);

