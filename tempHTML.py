'''
The purpose of this program is to create a dynamic html file in the static folder
The html file changes depending on what options you pass through parameters 
'''

import os

# the main call function (what you would call from other programs)
# calls tempHTML()
# calls strToFile()
def main(type, message, flag):
	html = tempHTML(type, message, flag)
	strToFile(html,"static/tempHTML.html")

# saves [text] to indicated [filename]
# creates file (if not already created), truncates it (deletes all information), and opens for reading and writing (we only will write to it)
# writes [text] to the file and closes it
def strToFile(text, filename):
	output = os.open( filename , os.O_CREAT | os.O_TRUNC | os.O_RDWR )
	os.write( output , text )
	os.close( output )

# concatenates strings
# takes an html template and adds parts depending on [type] and the [message]
# flag indicates what color the message is (ERROR (1) = RED, NO ERROR (0) = GREY)
# returns a string of the concatenated text
def tempHTML(type, message, flag):
	main_html_top ='''<!DOCTYPE HTML>
	<!--
		Web Aplication for Dot-Slash Computer Science club at Ohlone College by Cameron Kurotori
		HTML Template: Identity by HTML5 UP
			html5up.net | @ajlkn
			Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
	-->
	<html>
		<head>
			<title>Dot-Slash Computer Science</title>
			<meta charset="utf-8" />
			<meta name="viewport" content="width=device-width, initial-scale=1" />
			<!--[if lte IE 8]><script src="static/assets/js/html5shiv.js"></script><![endif]-->
			<link rel="stylesheet" href="static/assets/css/main.css" />
			<link rel="shortcut icon" href="static/favicon.ico">
			<!--[if lte IE 9]><link rel="stylesheet" href="static/assets/css/ie9.css" /><![endif]-->
			<!--[if lte IE 8]><link rel="stylesheet" href="static/assets/css/ie8.css" /><![endif]-->
			<noscript><link rel="stylesheet" href="static/assets/css/noscript.css" /></noscript>
		</head>
		<body class="is-loading">
			<!-- Wrapper -->
				<div id="wrapper">
					<!-- Main -->
						<section id="main">
							<header>
								<img src = "static/images/dotslash.png" alt="Dot Slash Logo" style="width:80%; max-width:800px" align=:middle"><br><br><br>'''
	main_html_bot = '''
								<footer>
							</footer>
						</section>
					<!-- Footer -->
						<footer id="footer">
							<ul class="copyright">
								<li>&copy; CAMERON KUROTORI</li><li>Design: <a href="http://html5up.net">HTML5 UP</a></li>
							</ul>
						</footer>
				</div>
			<!-- Scripts -->
				<!--[if lte IE 8]><script src="static/assets/js/respond.min.js"></script><![endif]-->
				<script>
					if ('addEventListener' in window) {
						window.addEventListener('load', function() { document.body.className = document.body.className.replace(/is-loading/, ''); });
						document.body.className += (navigator.userAgent.match(/(MSIE|rv:11\.0)/) ? ' is-ie' : '');
					}
				</script>
		</body>
	</html>'''
	variable = ''''''
	if type == "admin":
		variable = '''
									<h2>ADMINISTRATOR LOGIN</h2>
								</header>
								<hr />
								<p style="color:{flag_c}">{message}</p>
								<form action="/main" method="post">
									<div class="field">
										<input type="text" id="adminU" name="adminU" /><label for="adminU">ADMIN USERNAME</label><br>
										<input type="password" id="adminP" name="adminP" /><label for="adminP">ADMIN PASSWORD</label><br>
									</div>
									<ul class="actions">
										<li><input type="submit" name="Enter">&#160;&#160;&#160;&#160;&#160;&#160;<input type="reset" name="Reset"></li>
									</ul>
								</form>'''
	elif type == "checkIn":
		variable = '''
							<h2>CLUB MEETING CHECK-IN</h2>
						</header>
						<hr />
						<p style="color:{flag_c}">{message}</p>
						<form action="/checkInPrompt" method="post">
							<div class="field">
								<input type="radio" id="new" name="member" value="new"><label for="new">NEW MEMBER</label><br>
								<input type="radio" id="returning" name="member" value="returning"><label for="returning">RETURNING MEMBER</label><br>
								<input type="radio" id="update" name="member" value="update"><label for="update">UPDATE INFORMATION/FORGOT USERNAME (RETURNING MEMBERS)</label><br>
							</div>
							<ul class="actions">
								<li><input type="submit" name="Enter">&#160;&#160;&#160;&#160;&#160;&#160;<input type="reset" name="Reset"></li>
							</ul>
						</form>
						<hr />
						<form action="/home" method="post">
							<input type="submit" class="fit" name="menu" value="Main Menu">
						</form>'''
	elif type == "new":
		variable = '''
							<h2>NEW MEMBER CHECK-IN</h2>
						</header>
						<hr />
						<p style="color:{flag_c}">{message}</p>
						<form action="/newMember" method="post">
							<div class="field">
								<input type="text" id="first" name="first" /><label for="first">FIRST NAME*</label><br>
								<input type="text" id="last" name="last" /><label for="last">LAST NAME*</label><br>
								<input type="text" id="uname" name="uname" /><label for="uname">CHOOSE A USERNAME*</label><br>
								<input type="text" id="email" name="email" /><label for="email">EMAIL*</label><br>
								<input type="text" id="phone" name="phone" /><label for="phone">PHONE NUMBER</label><br>
								<input type="text" id="github" name="github" /><label for="github">GITHUB USERNAME</label><br>
							</div>
							<ul class="actions">
								<li><input type="submit" name="Enter">&#160;&#160;&#160;&#160;&#160;&#160;<input type="reset" name="Reset"></li>
							</ul>
						</form>
						<hr />
						<form action="/home" method="post">
							<input type="submit" class="fit" name="menu" value="Main Menu">
						</form>'''
	elif type == "returning":
		variable = '''							
							<h2>RETURNING MEMBER CHECK-IN</h2>
						</header>
						<hr />
						<p style="color:{flag_c}">{message}</p>
						<form action="/returningMember" method="post">
							<div class="field">
								<input type="text" id="uname" name="uname" /><label for="uname">USERNAME*</label><br>
							</div>
							<ul class="actions">
								<li><input type="submit" name="Enter">&#160;&#160;&#160;&#160;&#160;&#160;<input type="reset" name="Reset"></li>
							</ul>
						</form>
						<hr />
						<form action="/home" method="post">
							<input type="submit" class="fit" name="menu" value="Main Menu">
						</form>'''
	elif type == "update":
		variable = '''
							<h2>RETURNING MEMBER INFORMATION UPDATE</h2>
						</header>
						<hr />
						<p style="color:{flag_c}">{message}</p>
						<form action="/updateInformation" method="post">
							<div class="field">
								<input type="text" id="first" name="first" /><label for="first">FIRST NAME*</label><br>
								<input type="text" id="last" name="last" /><label for="last">LAST NAME*</label><br>
								WHAT WOULD YOU LIKE TO UPDATE?
								<select name="field">
									<option value="username">USERNAME</option>
									<option value="email">EMAIL</option>
									<option value="phone_number">PHONE NUMBER</option>
									<option value="github">GITHUB USERNAME</option>
								</select><br>
								<input type="text" id="updatedInfo" name="updatedInfo" /><label for="updatedInfo">UPDATED INFORMATION*</label><br>
							</div>
							<ul class="actions">
								<li><input type="submit" name="update" value="Update">&#160;&#160;&#160;&#160;&#160;&#160;<input type="reset" name="reset" value="Reset"></li>
							</ul>
						</form>
						<hr />
						<form action="/home" method="post">
							<input type="submit" class="fit" name="menu" value="Main Menu">
						</form>'''
	if flag == 0:
		flag_c = "grey"
	elif flag == 1:
		flag_c = "red"
	f_variable = variable.format(**locals())
	html = main_html_top + f_variable + main_html_bot
	return html

