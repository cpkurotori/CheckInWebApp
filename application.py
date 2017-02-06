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
	tempHTML.main("admin", "")
	return application.send_static_file("tempHTML.html")

@application.route("/main", methods=["post"])
def main():
	adminU = request.form['adminU']
	adminP = request.form['adminP']
	if (adminU == dbcredentials.getAdminU()) and (adminP == dbcredentials.getAdminP()):
		tempHTML.main("checkIn", "")
	else:
		tempHTML.main("admin", "Incorrect username or password. Please try again.")
	return application.send_static_file("tempHTML.html")


@application.route("/home", methods=["post"])
def home():
	tempHTML.main("checkIn", "")
	return application.send_static_file("tempHTML.html")

@application.route("/checkInPrompt", methods=["post"])
def checkInPrompt():
	member = request.form['member']
	if member == "new":
		tempHTML.main("new", "")
	elif member == "returning":
		tempHTML.main("returning", "")
	elif member == "update":
		tempHTML.main("update", "")
	return application.send_static_file("tempHTML.html")

@application.route("/newMember", methods=["post"])
def newMember():
	first = request.form['first']
	last = request.form['last']
	uname = request.form['uname']
	email = request.form['email']
	phone = request.form['phone']
	test = checkIn.checkDuplicate(mysql,"MemberInformation","username",uname)
	now = datetime.datetime.now()
	date = now.strftime("%Y-%m-%d")
	if test==True:
		tempHTML.main("new", "Username already exists. Please choose a different username.")
	else:
		checkIn.createNew (mysql, first, last, uname, email, phone, date)
		checkIn.checkIn (mysql, uname, date)
		tempHTML.main("checkIn", "")
	return application.send_static_file("tempHTML.html")

@application.route("/returningMember", methods=["post"])
def returningMember():
	uname = request.form['uname']
	test = checkIn.checkDuplicate (mysql,"MemberInformation","username",uname)
	now = datetime.datetime.now()
	date = now.strftime("%Y-%m-%d")
	if test==False:
		tempHTML.main("returning", "Member not found. Please try again, or go to the Main Menu and either register as a new member, or update your user profile.")
	else:
		tempHTML.main("checkIn", "")
	return application.send_static_file("tempHTML.html")

@application.route("/updateInformation", methods=["post"])
def updateInformation():
	first = request.form['first']
	last = request.form['last']
	field = request.form['field']
	updatedInfo = request.form['updatedInfo']
	now = datetime.datetime.now()
	date = now.strftime("%Y-%m-%d")
	test = checkIn.checkNameDuplicate (mysql,first,last)
	if test==True:
		checkIn.updateInfo (mysql,first,last,field,updatedInfo)
		tempHTML.main("checkIn", "")
	else:
		tempHTML.main("update", "Member not found. Please try again. NOTE: First name and lastname are case-sensitive (i.e. if you originally checked-in using all lowercase, you must enter all lowercase)")
	return application.send_static_file("tempHTML.html")

# run the application.
if __name__ == "__main__":
	# Setting debug to True enables debug output. This line should be
	# removed before deploying a production application.
	application.debug = True
	application.run()