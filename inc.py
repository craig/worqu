#!/usr/bin/env python
# open db connection
import cgitb; cgitb.enable()

# connect to the database, warning: it won't get closed automatically.
def dbconnect():
	import psycopg2 as dbapi2
	db = dbapi2.connect (database="worqu", user="worqu", password="worqu", host="localhost", port="5432")
	return db

