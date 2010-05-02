/*

Needs postgresql. Import with: psql < scheme.sql

*/

DROP database worqu;
CREATE DATABASE worqu OWNER worqu;
\c worqu;
GRANT ALL ON DATABASE worqu to worqu;

CREATE TABLE category (
cid		SERIAL		NOT NULL UNIQUE,
text		varchar(16)	NOT NULL
);
INSERT INTO category (text) VALUES ('Intern');
INSERT INTO category (text) VALUES ('Kundenprojekt');

CREATE TABLE task (
tid		SERIAL		NOT NULL UNIQUE PRIMARY KEY,
category	int		NOT NULL REFERENCES category(cid),
perc		int		NOT NULL,
prio		int		NOT NULL,
taskdesc	varchar(256)	NOT NULL,
createts	timestamp	NOT NULL,
endtime		timestamp	NOT NULL,
url		varchar(256),
position	int		NOT NULL
);
INSERT INTO task (createts,category,prio,perc,endtime,taskdesc,url,position) VALUES (now(), 1, 1, 0, '2010-03-11', 'Fix Firewall', 'http://your.bug.tracker/1', 0);
INSERT INTO task (createts,category,prio,perc,endtime,taskdesc,url,position) VALUES (now(), 1, 2, 1, '2010-03-11', 'Clean the room', 'http://your.bug.tracker/2', 0);

CREATE TABLE person (
pid		SERIAL		NOT NULL UNIQUE PRIMARY KEY,
name		varchar(32)	NOT NULL UNIQUE
);
INSERT INTO person (name) VALUES ('Craig');
INSERT INTO person (name) VALUES ('User2');


CREATE TABLE persontask (
personid	int		NOT NULL REFERENCES person(pid),
taskid		int		NOT NULL UNIQUE REFERENCES task(tid)
);
INSERT INTO persontask (personid, taskid) VALUES (1,1);
INSERT INTO persontask (personid, taskid) VALUES (2,2);

CREATE TABLE prioattr (
prio		int		NOT NULL,
priodesc	varchar(16)	NOT NULL,
color		varchar(16)	NOT NULL
);
INSERT INTO prioattr (prio,priodesc,color) VALUES (1,'urgent','red');
INSERT INTO prioattr (prio,priodesc,color) VALUES (2,'high','tomato');
INSERT INTO prioattr (prio,priodesc,color) VALUES (3,'normal','#FFFF66');
INSERT INTO prioattr (prio,priodesc,color) VALUES (4,'low','lightgreen');

GRANT ALL ON person TO worqu;
GRANT ALL ON persontask TO worqu;
GRANT ALL ON task TO worqu;
GRANT ALL ON category TO worqu;
GRANT ALL ON task TO worqu;
GRANT ALL ON prioattr TO worqu;
GRANT ALL ON task_tid_seq to worqu;


