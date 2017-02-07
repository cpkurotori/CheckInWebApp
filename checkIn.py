from flask.ext.mysql import MySQL
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
# querys to find any elements in MemberInformation table with the a first name matching [first] and a last name matching [last]
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
		return False	#indicated name not found

def updateInfo (mysql, first, last, field, updatedInfo):
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT roster_id FROM MemberInformation WHERE firstname=\""+str(first)+"\" AND lastname=\""+str(last)+"\"")
	id = cursor.fetchall()[0][0]			# stores the query results
	cursor.execute("UPDATE MemberInformation SET "+str(field)+"=\""+str(updatedInfo)+"\" WHERE roster_id="+str(id))
	conn.commit()
	cursor.close()
	conn.close()

def getName (mysql, username):
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT firstname FROM MemberInformation WHERE username=\""+str(username)+"\"")
	firstname = cursor.fetchall()[0][0]
	cursor.close()
	conn.close()
	return firstname