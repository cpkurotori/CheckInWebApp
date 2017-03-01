'''
The purpose of this program is to define functions that involve commands to the MySQL database (i.e. update tables, insert to tables, check counts in tables, etc)
'''


from flaskext.mysql import MySQL
import os

# connects to mysql database, creates cursor
# insert element in MemberInformation table with [first], [last], [uname], [email], [phone] and [date]
# commits the changes to the database
# close cursor and connection
def createNew (mysql, first, last, uname, email, phone, date):
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("INSERT INTO MemberInformation (firstname, lastname, username, email, phone_number, date_joined) VALUES (\""+first+"\",\""+last+"\",\""+uname+"\",\""+email+"\",\""+phone+"\",\""+date+"\")")
	conn.commit()
	cursor.close()
	conn.close()

# connects to mysql database, creates cursor
# finds roster_id of person with matching uname
# inserts element in MemberInformation table with found roster_id an [date]
# commits the changes to the database
# close cursor and connection
def checkIn (mysql, uname, date):
	# selects the roster id of the person wtih the username that matches the  parameter uname
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT roster_id FROM MemberInformation WHERE username=\""+str(uname)+"\"")
	id = cursor.fetchall()[0][0]			# stores the query results
	cursor.execute("INSERT INTO Attendance (roster_id,date) VALUES("+str(id)+",\""+str(date)+"\")")
	conn.commit()
	cursor.close()
	conn.close()

# connects to mysql database, creates cursor
# querys to find any elements in [table] with the a value in the [field] column that matches [test]
# 0 for not found - close cursor and connection and return True
# !0 for found - close cursor and connection and return False

def checkDuplicate (mysql, table, field, test):
	conn = mysql.connect()
	cursor = conn.cursor()	
	cursor.execute("SELECT COUNT(*) FROM "+table+" WHERE "+str(field)+"=\""+str(test)+"\"")
	count = cursor.fetchall()[0][0]
	if count != 0:
		cursor.close()
		conn.close()	
		return True		#indicates duplicate is found
	else:
		cursor.close()
		conn.close()		
		return False	#indicated no duplicate is found

# connects to mysql database, creates cursor
# querys to find any elements in MemberInformation table with the a firstname matching [first] and a lastname matching [last]
# 0 for not found - close cursor and connection and return False
# 1 for found - close cursor and connection and return True
def checkNameDuplicate (mysql, first, last,):
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT COUNT(*) FROM MemberInformation WHERE firstname=\""+str(first)+"\" AND lastname=\""+last+"\"")
	count = cursor.fetchall()[0][0]
	if count == 1:
		cursor.close()
		conn.close()
		return True		#indicates name found
	else:
		cursor.close()
		conn.close()
		return False	#indicates name not found

# connects to mysql database, creates cursor
# updates information in MemberInformation table with firstname matching [first] and lastname matching [last]
# commits the changes and closes cursor and connection

def updateInfo (mysql, first, last, field, updatedInfo):
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("UPDATE MemberInformation SET "+str(field)+"='"+str(updatedInfo)+"' WHERE firstname=\""+str(first)+"\" AND lastname=\""+str(last)+"\"")
	conn.commit()
	cursor.close()
	conn.close()

# connects to mysql database, creates cursor
# querys to find the firstname of any elements with username matching [username]
# closes cursor and connection
# returns firstname string
def getName (mysql, username):
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT firstname FROM MemberInformation WHERE username=\""+str(username)+"\"")
	firstname = cursor.fetchall()[0][0]
	cursor.close()
	conn.close()
	return firstname

# connects to mysql database, creates cursor
# querys for a count of entries that have a date (on Attendance) matching with [date] and a username (on MemberInformation) matching with [username]
# 0 for none - close cursor and connection and return False
# !0 for at least one found - close cursor and connection and return True
def duplicateCheckIn (mysql, username, date):
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT COUNT(*) FROM Attendance a LEFT JOIN MemberInformation m ON m.roster_id=a.roster_id WHERE m.username='"+str(username)+"' AND a.date='"+str(date)+"'")
	count = cursor.fetchall()[0][0]			# stores the query results
	if count == 0:
		cursor.close()
		conn.close()
		return False	#indicates no other entries with that username on that date -> okay to checkin
	else:
		cursor.close()
		conn.close()
		return True		#indicates another entry with that username on that date -> do not check-in