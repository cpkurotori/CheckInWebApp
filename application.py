from flask import Flask, request
from flask.ext.mysql import MySQL
import checkIn, datetime, dbcredentials

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
	return application.send_static_file("checkIn.html")

@application.route("/home", methods=["post"])
def home():
	return application.send_static_file("checkIn.html")

@application.route("/checkInPrompt", methods=["post"])
def checkInPrompt():
	member = request.form['member']
	if member == "new":
		return application.send_static_file("newmember.html")
	elif member == "returning":
		return application.send_static_file("returningmember.html")
	elif member == "update":
		return application.send_static_file("updateinformation.html")

@application.route("/newMember", methods=["post"])
def newMember():
	first = request.form['first']
	last = request.form['last']
	uname = request.form['uname']
	email = request.form['email']
	phone = request.form['phone']
	test = checkIn.checkDuplicate (mysql, "username",uname)
	now = datetime.datetime.now()
	date = now.strftime("%Y-%m-%d")
	if test==True:
		return application.send_static_file("newmember.html")
	else:
		checkIn.createNew (mysql, first, last, uname, email, phone, date)
		checkIn.checkIn (mysql, uname, date)
	return application.send_static_file("checkIn.html")

@application.route("/returningMember", methods=["post"])
def returningMember():
	uname = request.form['uname']
	test = checkIn.checkDuplicate (mysql,"username",uname)
	now = datetime.datetime.now()
	date = now.strftime("%Y-%m-%d")
	if test==False:
		return application.send_static_file("returningmember.html")
	else:
		checkIn.checkIn (mysql, uname, date)
	return application.send_static_file("checkIn.html")

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
	else:
		return application.send_static_file("updateinformation.html")
	return application.send_static_file("checkIn.html")

# run the application.
if __name__ == "__main__":
	# Setting debug to True enables debug output. This line should be
	# removed before deploying a production application.
	# application.debug = True
	application.run()