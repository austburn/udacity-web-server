import os
import webapp2
import jinja2
import time
import cgi

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
		
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class BlogPost(db.Model):
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):
	def get(self):
		posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC")

		self.render("blog.html", posts = posts)

class FormPage(Handler):
	def render_form(self, subject="", content="", error=""):
		self.render("form.html", subject = subject, content = content, error = error)

	def get(self):
		self.render_form()

	def post(self):
		subject = cgi.escape(self.request.get("subject"), quote = True)
		content = cgi.escape(self.request.get("content"), quote = True)

		if subject and content:
			b = BlogPost(subject = subject, content = content)

			b.put()

			self.redirect('/blog/%d' % b.key().id())
		else:
			error = "I need a subject and post!"
			self.render_form(subject, content, error)

class BlogPage(Handler):
	def get(self, blog_id):
		post = BlogPost.get_by_id(int(blog_id))
		self.render("blogpost.html", subject=post.subject, content=post.content)

app = webapp2.WSGIApplication([
	('/blog', MainPage),
	('/blog/newpost', FormPage),
	(r'/blog/(\d+)', BlogPage)],
	debug=True)