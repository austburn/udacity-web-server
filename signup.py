#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re

form="""
<form method="post">
	<span>
		<strong>Name:</strong>
	</span>
	<input type="text" name="name" value="%(name)s"><span class="error">%(name_err)s</span>
	<br/>

	<span>
		<strong>Password:</strong>
	</span>
	<input type="password" name="pass"><span class="error">%(password_err)s</span>
	<br/>

	<span>
		<strong>Verify Password:</strong>
	</span>
	<input type="password" name="verify"><span class="error">%(ver_pass_err)s</span>
	<br/>

	<span>
		<strong>Email:</strong>
	</span>
	<input type="text" name="email"><span class="error">%(email_err)s</span>
	<br/>

	<input type="submit">
</form>
"""

welcome="""
	<span>Welcome, %s</span>
"""

user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
pass_re = re.compile(r"^.{3,20}$")
email_re = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(name):
	return user_re.match(name)

def get_username(name):
	if (valid_username(name)):
		return name
	else:
		return "That's not a valid username."

def valid_password(password):
	return pass_re.match(password)

def get_password(password):
	if (valid_password(password)):
		return ""
	else:
		return "That's not a valid password."

def pass_match(pass1, pass2):
	if (pass1 == pass2):
		return True
	else:
		return False

def get_pass_match(pass1, pass2):
	if (pass_match(pass1, pass2)):
		return ""
	else:
		return "Passwords do not match."

def valid_email(email):
	return email_re.match(email) or email == ''

def get_email(email):
	if (valid_email(email)):
		return email
	else:
		return "That's not a valid email."



class MainPage(webapp2.RequestHandler):
	def write_form(self, name="", name_err="", password_err="", ver_pass_err="", email_err=""):
		self.response.out.write(form % {"name" : name,
										"name_err" : name_err,
										"password_err" : password_err,
										"ver_pass_err" : ver_pass_err,
										"email_err" : email_err})

	def get(self):
		self.write_form()

	def post(self):
		name = self.request.get('name')
		password = self.request.get('pass')
		ver_pass = self.request.get('verify')
		email = self.request.get('email')

		welcome_url = '/welcome?q=%s'

		if (valid_username(name) and valid_password(password) and pass_match(password, ver_pass) and valid_email(email)):
			self.redirect(welcome_url % name)
		else:
			self.write_form(name, 
							get_username(name), 
							get_password(password), 
							get_pass_match(password, ver_pass), 
							get_email(email))


class WelcomePage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write(welcome % self.request.get('q'))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/welcome', WelcomePage)
], debug=True)