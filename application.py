'''
This program uses a Flask webapplication framework.
The purpose of this program is to check in club members (or anything in your own circumstances) and store the data in a MySQL database
This program redirects webbrowsers to the necessary html files to display
'''



from flask import Flask, request
from flaskext.mysql import MySQL
import checkIn, datetime, dbcredentials, tempHTML

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# set-up mysql database configuration (database name, hostname, username, and password)
# calls functions from dbcredentials.py that hold the credential login infomation
mysql = MySQL()
application.config['MYSQL_DATABASE_DB'] = dbcredentials.getDatabase()
application.config['MYSQL_DATABASE_HOST'] = dbcredentials.getHost()
application.config['MYSQL_DATABASE_USER'] = dbcredentials.getUser()
application.config['MYSQL_DATABASE_PASSWORD'] = dbcredentials.getPass()
mysql.init_app(application)

# [index] - main page
# calls tempHTML.py to create the admin login page with no errors and no message
# returns to the webbrowser (using Flask) the tempHTML.html page that was created
@application.route("/")
def index():
	tempHTML.main("admin", "", 0)
	return application.send_static_file("tempHTML.html")

# main page - admin page
# requests information from the username and password fields
# checks if the login credentials match the credentials identified in dbcredentials.py
# if credentials match, call tempHTML.py to create checkIn page with no error no message
# returns to the webbrowser (using Flask) the tempHTML.html page that was created
@application.route("/main", methods=["post"])
def main():
	adminU = request.form['adminU']
	adminP = request.form['adminP']
	if (adminU == dbcredentials.getAdminU()) and (adminP == dbcredentials.getAdminP()):
		tempHTML.main("checkIn", "", 0)
	else:
		tempHTML.main("admin", "Incorrect username or password. Please try again.", 1)
	return application.send_static_file("tempHTML.html")

# home page - member check in prompt page
# call tempHTML.py to create checkIn page with no error no message
# returns to the webbrowser (using Flask) the tempHTML.html page that was created
@application.route("/home", methods=["post"])
def home():
	tempHTML.main("checkIn", "", 0)
	return application.send_static_file("tempHTML.html")

# checkInPrompt - selected member check in page/update page (if error: member check in prompt page)
# requests the member field to see selection (if no selection, create check in page  with error and message indicating error)
# creates html page depending on user selection
# returns to the webbrowser (using Flask) the tempHTML.html page that was created
@application.route("/checkInPrompt", methods=["post"])
def checkInPrompt():
	try:
		member = request.form['member']
		if member == "new":
			tempHTML.main("new", "", 0)
		elif member == "returning":
			tempHTML.main("returning", "", 0)
		elif member == "update":
			tempHTML.main("update", "", 0)
	except:
		tempHTML.main("checkIn", "Please select an option below.", 1)
	return application.send_static_file("tempHTML.html")

# newMember  - member check in prompt page (if error: new member check in page)
# requests all the fields and assigns them to respective variables (if required fields empty, create new member check in page with error and message indicating error )
# checks if duplicate username exists (if duplicate exists, create new member check in page with error and message indicating error)
# calls createNew() and checkIn() from checkIn.py
# creates html page - member check in prompt page with no error and message indicating they have been checked in
# returns to the webbrowser (using Flask) the tempHTML.html page that was created
@application.route("/newMember", methods=["post"])
def newMember():
	first = request.form['first']
	last = request.form['last']
	uname = request.form['uname'] 
	email = request.form['email']
	phone = request.form['phone']
	if first =="" or last == "" or uname == "" or email == "":
		tempHTML.main("new", "Please fill-in every required field", 1)	
	else:		
		test = checkIn.checkDuplicate(mysql,"MemberInformation","username",uname)
		now = datetime.datetime.now()
		date = now.strftime("%Y-%m-%d")
		if test==True:
			tempHTML.main("new", "Username already exists. Please choose a different username.", 1)
		else:
			checkIn.createNew (mysql, first, last, uname, email, phone, date)
			checkIn.checkIn (mysql, uname, date)
			f_name= checkIn.getName (mysql, uname)
			message = "Thank you, "+str(f_name)+". You've been registered and checked in for "+str(date)+"!"
			tempHTML.main("checkIn", message, 0)
	return application.send_static_file("tempHTML.html")

# returningMember - member check in prompt page (if error: returning member check in page)
# requests all the fields and assigns them to respective variables (if required fields empty, create returning member check in page with error and message indicating error )
# calls checkDuplicate from checkIn.py (if duplicate does not exists, creates new member check in page with error and message indicating error)
# if duplicate exists --> calls duplicateCheckIn() from checkIn.py (if duplicate exists, creates member check in prompt page with no error and message saying user was already checked in)
# if duplicate does not exist --> calls checkIn() from checkIn.py
# creates html page - member check in prompt page with no error and message indicating they have been checked in
# returns to the webbrowser (using Flask) the tempHTML.html page that was created
@application.route("/returningMember", methods=["post"])
def returningMember():
	uname = request.form['uname']
	if uname == "":
		tempHTML.main("returning", "Please fill-in every required field",1)
	else:
		now = datetime.datetime.now()
		date = now.strftime("%Y-%m-%d")
		test = checkIn.checkDuplicate (mysql,"MemberInformation","username",uname)
		if test==False:
			tempHTML.main("returning", "Member not found. Please try again, or go to the Main Menu and either register as a new member, or update your user profile.", 1)
		else:
			alreadyHere = checkIn.duplicateCheckIn (mysql, uname, date)
			if alreadyHere == True:
				tempHTML.main("checkIn", "That user is already checked in.", 0)
			else:
				checkIn.checkIn (mysql, uname, date)
				f_name= checkIn.getName (mysql, uname)
				message = "Thank you, "+str(f_name)+". You've been checked in for "+str(date)+"!"
				tempHTML.main("checkIn", message, 0)
	return application.send_static_file("tempHTML.html")

# returningMember updateInformation- member check in prompt page (if error: update page)
# requests all the fields and assigns them to respective variables (if required fields empty, create update page with error and message indicating error )
# checks if there is an element in the database with btoh the first naem and last name exists (if element does not exists, create update page with error and message indicating error)
# calls updateInfo() from checkIn.py
# creates html page - member check in prompt page with no error and message indicating updates have been made
# returns to the webbrowser (using Flask) the tempHTML.html page that was created
@application.route("/updateInformation", methods=["post"])
def updateInformation():
	first = request.form['first']
	last = request.form['last']
	field = request.form['field']
	updatedInfo = request.form['updatedInfo']
	now = datetime.datetime.now()
	date = now.strftime("%Y-%m-%d")
	if first == "" or last == "" or updatedInfo == "":
		tempHTML.main("update", "Please fill-in every required field", 1)		
	else:
		test = checkIn.checkNameDuplicate (mysql,first,last)
		if test==True:
			checkIn.updateInfo (mysql,first,last,field,updatedInfo)
			message = "Thank you, "+str(first)+". Your "+field+" has been updated! If you need still need to check-in, please do so from here!"
			tempHTML.main("checkIn", message, 0)
		else:
			tempHTML.main("update", "Member not found. Please try again.", 1)
	return application.send_static_file("tempHTML.html")

# run the application.
if __name__ == "__main__":
	# Setting debug to True enables debug output. This line should be
	# removed before deploying a production application.
	#application.debug = True
	application.run()