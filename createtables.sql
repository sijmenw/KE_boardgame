CREATE TABLE boardgame (
boardgame_id int,
name varchar(100) NOT NULL,
description varchar(1500),
expansion boolean,
min_players int,
max_players int,
min_age int,
playing_time int, 
average_rating float,
PRIMARY KEY(boardgame_id)
);

CREATE TABLE boardgame_category (
boardgame_id int NOT NULL,
category varchar(100) NOT NULL,
PRIMARY KEY(boardgame_id, category)
);

CREATE TABLE boardgame_mechanics (
boardgame_id int NOT NULL,
mechanics varchar(100) NOT NULL,
PRIMARY KEY(boardgame_id, mechanics)
);

CREATE TABLE boardgame_designer (
boardgame_id int NOT NULL,
designer varchar(100) NOT NULL,
PRIMARY KEY(boardgame_id, designer)
);

CREATE TABLE boardgame_publisher (
boardgame_id int NOT NULL,
publisher varchar(100) NOT NULL,
PRIMARY KEY(boardgame_id, publisher)
);

CREATE TABLE boardgame_expands (
boardgame_id int NOT NULL,
expands_boardgame_id int NOT NULL,
PRIMARY KEY(boardgame_id, expands_boardgame_id)
);

CREATE TABLE boardgame_expansion (
boardgame_id int NOT NULL,
expansion_id int NOT NULL,
PRIMARY KEY(boardgame_id, expansion_id)
);