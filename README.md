#A Check-In/Attendance Tracker Web Application

Out of the need for a check-in program, this program was created to maintain a database of members and their attendence to club meetings. This application is written in python and utilizes a flask framework for the web application. A live version of the webapp can be found at http://checkin.dot-slash-cs.club.

##Requirements
This web application requires the following packages:
- appdirs==1.4.0
- Flask==0.10.1
- Flask-MySQL==1.4.0
- itsdangerous==0.24
- Jinja2==2.9.5
- MarkupSafe==0.23
- packaging==16.8
- PyMySQL==0.7.9
- pyparsing==2.1.10
- six==1.10.0
- Werkzeug==0.11.15

##application.py
This file contains the code that runs the flask app and sets up the necessary connection information to the MySQL database. Depending on the selections on the webpage, the necessary functions are called and the web browser is redirected to the new tempHTML.html located in the static directory

This file imports functions from checkIn.py, tempHTML.py and dbcredentials.py and utilizes the MySQL connector from flask.ext.mysql

##checkIn.py
This file contains functions that initialize the connection with the database and gathers information, change information, or add information (depending on necessary function).

This file utilizes the MySQL connector from flask.ext.mysql

##tempHTML.py
This files contains the code that creates an html from a basic template for the necessary webpage (prompts for New Member Check In, Returning Member Check In, etc). 

The new tempHTML.html is produced in the static directory

##dbcredentials.py
This code contains the credentials and infomation for the database and the admin login