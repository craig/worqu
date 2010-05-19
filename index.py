#!/usr/bin/env python
"""
This is Worqu, a simple web-based program to manage a queue of tasks.
Copyright (C) 2010 by Stefan Behte

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

You can contact me at stefan dot behte at gmx dot net
"""

import time, os, sys, cgi
import cgitb; cgitb.enable()
import hashlib, random
from subprocess import Popen, PIPE, call
import string

# escaping
from cgi import escape
from urllib import unquote

# database stuff
import inc
db=inc.dbconnect()
cur=db.cursor()

# Save form data
form = cgi.FieldStorage()

# user wants to edit
if form.has_key('edit'):
	print "Content-Type: text/html; charset=utf-8\n"

	edit = escape(unquote(str(form.getvalue("edit"))),1)

	### TEXT & URL
	print """ <form name="edit_text" action="/index.py" method="POST"> """

	try:
		cur.execute("SELECT taskdesc,url FROM task WHERE tid=%s;", (edit,) )
		rows = cur.fetchall()
		mytext = rows[0][0]
		myurl =  rows[0][1]
	except:
		mytext = ''
		myurl = ''

	print """
	<textarea name="edit_text" cols="40" rows="5">%s</textarea>
	<br/>
	<input name="edit_url" type="text" value="%s" size="36" maxlength="256">
	<br/>
	<input type="hidden" name="id" value="%s">
	""" % (mytext, myurl, edit)



	### ENDTIME
	cur.execute("SELECT endtime FROM task WHERE tid=%s;", (edit,) )
	try:
		endtime = cur.fetchall()[0][0]
	except:
		endtime = '2010-12-31 00:00:00'

	print """ <input name="edit_endtime" type="text" value="%s" size="18" maxlength="64"> <br/> """ % (endtime)


	### PRIO
	# get my own prio
	try:
		cur.execute("SELECT prio FROM task WHERE tid=%s;", (edit,) )
		myprio = cur.fetchall()[0][0];
	except:
		myprio = str('4')
	
	# get prio array
	cur.execute("SELECT prio, priodesc, color FROM prioattr ORDER by prio;" )
	rows = cur.fetchall();

	# preselect current prio
	for i in range(0, len(rows) ):
		if cmp(str(myprio), str(rows[i][0])) == 0:
			print """ <input type="radio" name="edit_prio" value="%s" checked>%s - %s</option><br/> """ % ( str(rows[i][0]), str(rows[i][0]), str(rows[i][1]))
		else:
			print """ <input type="radio" name="edit_prio" value="%s">%s - %s</option><br/> """ % ( str(rows[i][0]), str(rows[i][0]), str(rows[i][1]))

	print "<BR>"



	#### PERCENT
	try:
		cur.execute("SELECT perc FROM task WHERE tid=%s;", (edit,) )
		rows = cur.fetchall()[0][0];
	except:
		rows = ''

	print """ <select name="edit_perc" size="1"> """

	for i in range (0,101):
		if rows == i:
			print """ <option selected value="%s">%s</option> """ % (i,i)
		else:			
			print """ <option value="%s">%s</option> """ % (i,i)

	print """</select><b> %</b><br/>"""



	#### PERSON ####
	
	# get all persons
	cur.execute("SELECT pid, name FROM person;")
	myuser = cur.fetchall();
	
	# get person that owns the task
	try:
		cur.execute("SELECT pid FROM persontask JOIN person ON persontask.personid = person.pid INNER JOIN task ON persontask.taskid = task.tid WHERE tid=%s;", (edit,) )
		curuser = cur.fetchall()[0][0];
	except:
		curuser = ''

	print """ <select name="edit_persontask" size="1"> """

	for i in range (1, len(myuser)+1):
		if myuser[i-1][0] == curuser:
			print """ <option selected value="%s">%s</option> """ % (i, myuser[i-1][1])
		else:			
			print """ <option value="%s">%s</option> """ % (i, myuser[i-1][1])
	print """
	</select>
	<br/>
	<br/>
	<input type="submit" value="ok" style="background-color: black; border:0px; padding:3px; color: #fff; font-weight:bold;" ></div>
	</form>	
	"""

	sys.exit(1)
	

if form.has_key('id'):

	id = escape(unquote(str(form.getvalue("id"))),1)

	if (id != '-1'):

		if form.has_key('up'):
			# Welcher Task hat die Position, an die ich moechte
			#cur.execute("SELECT tid FROM task WHERE position = (SELECT position FROM task WHERE tid=%s)+1;), (id,)"
			cur.execute("UPDATE task SET position = position + 1 WHERE tid=%s", (id,) )
			cur.execute("COMMIT;");

		if form.has_key('down'):
			cur.execute("UPDATE task SET position = position - 1 WHERE tid=%s", (id,) )
			cur.execute("COMMIT;");

		if form.has_key('edit_url'):
			url = escape(unquote(str(form.getvalue("edit_url"))),1)
			cur.execute("UPDATE task SET url = %s WHERE tid=%s", (url, id) )
			cur.execute("COMMIT;");

		if form.has_key('edit_text'):
			text = escape(unquote(str(form.getvalue("edit_text"))),1)
			cur.execute("UPDATE task SET taskdesc=%s WHERE tid=%s", (text, id) )
			cur.execute("COMMIT;");

		if form.has_key('edit_prio'):
			prio = escape(unquote(str(form.getvalue("edit_prio"))),1)
			cur.execute("UPDATE task SET prio=%s WHERE tid=%s", (prio, id) )
			cur.execute("COMMIT;");

		if form.has_key('edit_perc'):
			perc = escape(unquote(str(form.getvalue("edit_perc"))),1)
			cur.execute("UPDATE task SET perc=%s WHERE tid=%s", (perc, id) )
			cur.execute("COMMIT;");

		if form.has_key('edit_endtime'):
			endtime = escape(unquote(str(form.getvalue("edit_endtime"))),1)
			try:
				cur.execute("UPDATE task SET endtime=%s WHERE tid=%s", (endtime, id) )
				cur.execute("COMMIT;");
			except:
				print "Content-Type: text/html; charset=utf-8\n"
				print "<b>Something is wrong with your date.</b>"
				sys.exit(-1)

		if form.has_key('edit_persontask'):
			persontask = escape(unquote(str(form.getvalue("edit_persontask"))),1)
			cur.execute("UPDATE persontask SET personid=%s WHERE taskid=%s", (persontask, id) )
			cur.execute("COMMIT;");
		
	else:
		if form.has_key('edit_text'):

			text = escape(unquote(str(form.getvalue("edit_text"))),1)
				
			try:
				url = escape(unquote(str(form.getvalue("edit_url"))),1)
			except:
				url = ''

			try:
				perc = escape(unquote(str(form.getvalue("edit_perc"))),1)
			except:
				perc = '0'

			try:
				prio = escape(unquote(str(form.getvalue("edit_prio"))),1)
			except:
				prio = '4'

			try:
				endtime = escape(unquote(str(form.getvalue("edit_endtime"))),1)
			except:
				endtime = '2010-12-31 00:00:00'
				
			try:
				persontask = escape(unquote(str(form.getvalue("edit_persontask"))),1)
			except:
				persontask = '1'


			# a bit ugly ;)

			# get current time
			cur.execute("SELECT now()");
			now = cur.fetchall()[0][0]

			# create new task
			cur.execute("INSERT INTO task (createts,category,prio,perc,endtime,taskdesc,url,position) VALUES (%s, 1, %s, %s, %s, %s, %s, 0);", (now, prio, perc, endtime, text, url) )

			# get id of created task
			cur.execute("SELECT tid FROM task WHERE createts=%s", (now,));
			newtask = cur.fetchall()[0][0]

			# create mapping task <> persontask
			cur.execute("INSERT INTO persontask (personid, taskid) VALUES (%s, %s);", (persontask,newtask));
			cur.execute("COMMIT;");

			print "Content-Type: text/html; charset=utf-8\n"
			print "<b>Task created.</b>"

			sys.exit(1)

		else:
			print "Content-Type: text/html; charset=utf-8\n"
			print "<b>Your task description needs some text.</b>"
			sys.exit(1)

### Special case:
if form.has_key('del'):
	print "Content-Type: text/html; charset=utf-8\n"
	print """ <form name="edit_del" action="/index.py" method="POST"> """
	
	cur.execute("SELECT taskdesc FROM task WHERE tid=%s;", ( str(form['del'].value), ) )
	rows = cur.fetchall()[0][0];

	print """
	Task "%s" will be deleted.</BR>
	<BR>
	<input type="hidden" name="edit_del" value="urmum">
	<input type="hidden" name="id" value="%s">
	<input type="submit" value="ok" style="background-color: black; border:0px; padding:3px; color: #fff; font-weight:bold;" ></div>
	<input type="button" value="no" style="background-color: black; border:0px; padding:3px; color: #fff; font-weight:bold;" onClick="window.top.window.$.fancybox.close();"></div>
	</form>	
	""" % (rows, str(form['del'].value) )
	
	sys.exit(1)
	
if form.has_key('edit_del') and form.has_key('id'):
	id = escape(unquote(str(form.getvalue("id"))),1)
	cur.execute("DELETE FROM persontask WHERE taskid=%s", (str(id),) )
	cur.execute("UPDATE task SET perc=%s WHERE tid=%s", ( 100, str(id) ) )
	cur.execute("COMMIT;");

### redirect everything that has "id" set
if form.has_key('id'):
	print "Location: /index.py\n"
	sys.exit(1)


print "Content-Type: text/html; charset=utf-8\n"

# show header with random picture in the background 
f = open("templates/header", "r")
data = f.read()
try:
	files = os.listdir("img")
	rnr = random.randrange(0,len(files))
	imgfile = files[ rnr  ]
	data = data.replace("DUMMY_BACKGROUND",	"img/" + str(imgfile))
except:
	pass

print data
f.close()

# pre-fetching needed data
cur.execute("SELECT count(pid) FROM person;")
rows = cur.fetchall()[0][0];

cur.execute("SELECT prio, color FROM prioattr ORDER BY prio;")
color = cur.fetchall();

cur.execute("SELECT * FROM person;")
allusers = cur.fetchall();

if form.has_key('user'):
	user = escape(unquote(str(form.getvalue("user"))),1)
	cur.execute("SELECT pid, tid, taskdesc, to_char(endtime, 'YYYY-MM-DD'), perc, prio, url, position FROM persontask JOIN person ON persontask.personid = person.pid INNER JOIN task ON persontask.taskid = task.tid WHERE person.name=%s ORDER BY position DESC, prio ASC;", (user,) )
else:
	cur.execute("SELECT pid, tid, taskdesc, to_char(endtime, 'YYYY-MM-DD'), perc, prio, url, position FROM persontask JOIN person ON persontask.personid = person.pid INNER JOIN task ON persontask.taskid = task.tid ORDER BY position DESC, prio ASC;" )

rows = cur.fetchall();

# be careful with tasks, that are not linked; that's why we use len(rows) and not this:
# cur.execute("SELECT count(tid) FROM task;")
# tasknr = cur.fetchall()[0][0]

for i in range(0, len(rows)):
	f = open("templates/data", "r")
	data = f.read()

	# get user who owns the task
	u = rows[i][0] 
	data = data.replace("DUMMY_USER",	str(allusers[u-1][1]))

	# get color
	c =  rows[i][5]
	data = data.replace("DUMMY_BGCOLOR",	str(color[c-1][1]))

	data = data.replace("DUMMY_TASKID",	str(rows[i][1]))
	data = data.replace("DUMMY_TASKDESC",	str(rows[i][2]))
	data = data.replace("DUMMY_DATE",	str(rows[i][3]))
	data = data.replace("DUMMY_PERCENT",	str(rows[i][4]))
	data = data.replace("DUMMY_PRIO",	str(rows[i][5]))
	data = data.replace("DUMMY_URL",	str(rows[i][6]))
	data = data.replace("DUMMY_POS",	str(rows[i][7]))
	
	print data +  "</tr><tr>"

f = open("templates/footer", "r")
print f.read()
f.close()

# close database
cur.close
db.close

