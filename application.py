from flask import Flask, request
from flask.ext.mysql import MySQL
import checkIn, datetime, dbcredentials, tempHTML

# Open connection to the database using the login credentials of the given username and password parameters

# EB looks for an 'application' callable by default.

application = Flask(__name__)

mysql = MySQL()
application.config['MYSQL_DATABASE_DB'] = dbcredentials.getDatabase()
application.config['MYSQL_DATABASE_HOST'] = dbcredentials.getHost()
application.config['MYSQL_DATABASE_USER'] = dbcredentials.getUser()
application.config['MYSQL_DATABASE_PASSWORD'] = dbcredentials.getPass()
mysql.init_app(application)


@application.route("/")
def index():
	tempHTML.main("admin", "", 0)
	return application.send_static_file("tempHTML.html")

@application.route("/main", methods=["post"])
def main():
	adminU = request.form['adminU']
	adminP = request.form['adminP']
	if (adminU == dbcredentials.getAdminU()) and (adminP == dbcredentials.getAdminP()):
		tempHTML.main("checkIn", "", 0)
	else:
		tempHTML.main("admin", "Incorrect username or password. Please try again.", 1)
	return application.send_static_file("tempHTML.html")


@application.route("/home", methods=["post"])
def home():
	tempHTML.main("checkIn", "", 0)
	return application.send_static_file("tempHTML.html")

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

@application.route("/returningMember", methods=["post"])
def returningMember():
	uname = request.form['uname']
	if uname == "":
		tempHTML.main("returning", "Please fill-in every required field",1)
	else:
		test = checkIn.checkDuplicate (mysql,"MemberInformation","username",uname)
		now = datetime.datetime.now()
		date = now.strftime("%Y-%m-%d")
		if test==False:
			tempHTML.main("returning", "Member not found. Please try again, or go to the Main Menu and either register as a new member, or update your user profile.", 1)
		else:
			f_name= checkIn.getName (mysql, uname)
			message = "Thank you, "+str(f_name)+". You've been checked in for "+str(date)+"!"
			tempHTML.main("checkIn", message, 0)
	return application.send_static_file("tempHTML.html")

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
	application.debug = True
	application.run()