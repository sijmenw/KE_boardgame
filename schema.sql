drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  'text' text not null
);

drop table if exists games;
create table games (
  id integer primary key autoincrement,
  name text not null,
  type text not null
);

insert into games ('name', 'type') VALUES ('testName1', 'testType1');
insert into games ('name', 'type') VALUES ('testName2', 'testType2');
insert into games ('name', 'type') VALUES ('testName3', 'testType3');