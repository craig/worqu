/*

Needs postgresql. Import with: psql < scheme.sql

*/

\c worqu;

INSERT INTO category (text) VALUES ('Internal');
INSERT INTO category (text) VALUES ('Customer Project');

INSERT INTO task (createts,category,prio,perc,endtime,taskdesc,url,position) VALUES (now(), 1, 1, 10, '2010-03-11', 'Fix Firewall', 'http://your.bug.tracker/1', 0);
INSERT INTO task (createts,category,prio,perc,endtime,taskdesc,url,position) VALUES (now(), 1, 2, 20, '2010-03-11', 'Clean the room', 'http://your.bug.tracker/2', 0);
INSERT INTO task (createts,category,prio,perc,endtime,taskdesc,url,position) VALUES (now(), 1, 2, 30, '2010-03-11', 'Wash dishes', 'http://your.bug.tracker/3', 0);
INSERT INTO task (createts,category,prio,perc,endtime,taskdesc,url,position) VALUES (now(), 1, 3, 40, '2010-03-11', 'Buy new DVDs', 'http://your.bug.tracker/4', 0);
INSERT INTO task (createts,category,prio,perc,endtime,taskdesc,url,position) VALUES (now(), 1, 4, 40, '2010-03-11', 'Buy new server', 'http://computer.ebay.de/', 0);

INSERT INTO person (name) VALUES ('User1');
INSERT INTO person (name) VALUES ('User2');
INSERT INTO person (name) VALUES ('User3');
INSERT INTO person (name) VALUES ('User4');
INSERT INTO person (name) VALUES ('User5');

INSERT INTO persontask (personid, taskid) VALUES (1,1);
INSERT INTO persontask (personid, taskid) VALUES (2,2);
INSERT INTO persontask (personid, taskid) VALUES (3,3);
INSERT INTO persontask (personid, taskid) VALUES (4,4);
INSERT INTO persontask (personid, taskid) VALUES (5,5);

INSERT INTO toplink (url, descr) VALUES ('http://www.otrs.org','otrs');
INSERT INTO toplink (url, descr) VALUES ('http://dev.mysql.com/downloads/other/eventum/','eventum');
INSERT INTO toplink (url, descr) VALUES ('http://www.bugzilla.com','bugzilla');
INSERT INTO toplink (url, descr) VALUES ('http://www.nagios.com','nagios');
INSERT INTO toplink (url, descr) VALUES ('http://www.cacti.org','cacti');
INSERT INTO toplink (url, descr) VALUES ('http://www.ntop.org/ntop.html','ntop');


