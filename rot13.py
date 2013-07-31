import webapp2
import cgi
import logging

form="""
<form method=post>
	<textarea name="text">%s</textarea>

	<br>

	<input type="submit"></input>
</form>
"""

alphabet = {'a' : 'n',
			'b' : 'o',
			'c' : 'p',
			'd' : 'q',
			'e' : 'r',
			'f' : 's',
			'g' : 't',
			'h' : 'u',
			'i' : 'v',
			'j' : 'w',
			'k' : 'x',
			'l' : 'y',
			'm' : 'z',
			'n' : 'a',
			'o' : 'b',
			'p' : 'c',
			'q' : 'd',
			'r' : 'e',
			's' : 'f',
			't' : 'g',
			'u' : 'h',
			'v' : 'i',
			'w' : 'j',
			'x' : 'k',
			'y' : 'l',
			'z' : 'm'}

def escape_html(s):
	return cgi.escape(s, quote = True)

def rot13(text):
	s = list(text)
	counter = 0
	for c in s:
		if ord(c) > 64 and ord(c) < 91:
			s[counter] = chr(ord(alphabet[chr(ord(c) + 32)]) - 32)
		elif ord(c) > 96 and ord(c) < 123:
			s[counter] = alphabet[c]
		counter = counter + 1
	return "".join(s)

class MainPage(webapp2.RequestHandler):
	def write_form(self, string=""):
		self.response.out.write(form%string)

	def get(self):
		self.write_form()

	def post(self):
		s = self.request.get('text')
		s = rot13(s)
		s = escape_html(s)
		self.write_form(s)

app = webapp2.WSGIApplication([
	('/', MainPage)
], debug=True)