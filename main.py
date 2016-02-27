import cgi
import urllib
import webapp2
import jinja2
import os

from google.appengine.api import users
from google.appengine.ext import ndb
# from webapp2_extras import sessions

# All the data of my notes in a python file 
import mynotes


# Specify a path to a template directry
template_dir = os.path.join(os.path.dirname(__file__), "html_templates")
# Set up a jinja environment
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
							   extensions=["jinja2.ext.autoescape"],
							   autoescape = True)
# Register datetime format to the jinja environment
def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
	return value.strftime(format)
jinja_env.filters['datetimeformat'] = datetimeformat


class Handler(webapp2.RequestHandler):
	"""Generic handler"""
	def write(self, *a, **kw):
		# Write small strings to the website
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		# Render jinja2 templates
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		# Write the jinja template to the website
		return self.write(self.render_str(template, **kw))


DEFAULT_FEEDBACK_NAME = 'anonymous'

def feedback_key(feedback_name=DEFAULT_FEEDBACK_NAME):
	"""Constructs a Datastore key for a Feedback entity."""
	return ndb.Key('Feedback', feedback_name)


class Author(ndb.Model):
	"""Sub model for representing an author."""
	identity = ndb.StringProperty(indexed=False)
	email = ndb.StringProperty(indexed=False)


class Feedback(ndb.Model):
	"""A main model for representing an individual Feedback entry."""
	user_name = ndb.StructuredProperty(Author)
	user_comment = ndb.StringProperty(indexed=False)
	datetime = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(Handler):

	def get(self):
		self.render("index.html")


# class LogIn(BaseHandler):

# 	def get(self):
# 		if self.session.get("user"):
# 			del self.session["user"]
# 		if not self.session.get("referrer"):
# 			self.session["referrer"] = \
# 				self.request.environ["HTTP_REFERER"] \
# 				if "HTTP_REFERER" in self.request.environ \
# 				else "/"

# 		self.render("login.html")

# 	def post(self):
# 		user = self.request.get("user")
# 		self.session["user"] = user
# 		logging.info("%s just logged in" % user)
# 		self.redirect("/")


class LessonNotes(Handler):

	def get(self):
		# Calling data of my lesson notes from mynotes.py
		all_notes = mynotes.all_notes
		concepts_order = mynotes.concepts_order
		error = self.request.get("error", "")
		redirection = self.request.get("redirection", "")

		# Create multiple html file from one template
		

		# Render the data into the template "lessonnotes.html"
		self.render("lessonnotes.html",
					all_notes=all_notes,
					concepts_order=concepts_order)


def is_valid(user_input):
	if user_input.strip():
		return True
	else:
		return False


class FeedbackPage(Handler):

	def escape_html(s):
		return cgi.escape(s, quote = True)

	def get(self):
		feedback_name = self.request.get('feedback_named', DEFAULT_FEEDBACK_NAME)
		# [START query]
		# Query the Datastore and order earliest date first
		datetime = Feedback.datetime
		feedback_query = Feedback.query(
			ancestor=feedback_key(feedback_name)).order(-datetime)

		# Return a list of max 10 post objects. 
		maximum_fetch_size = 10
		feedback_list = feedback_query.fetch(maximum_fetch_size)
		# [END query]

		user = users.get_current_user()
		if user:
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		error = self.request.get("error", "")
		success = self.request.get("success", "")

		self.render("feedback.html",
					feedback_list=feedback_list,
					success=success,
					error=error,
					user=user,
					feedback_name=urllib.quote_plus(feedback_name),
					url=url,
					url_linktext=url_linktext)


	def post(self):

		feedback_name = self.request.get('feedback_name', DEFAULT_FEEDBACK_NAME)
		feedback = Feedback(parent=feedback_key(feedback_name))

		if users.get_current_user():
			feedback.user_name = Author(
				identity=users.get_current_user().user_id(),
				email=users.get_current_user().email())

		user_comment = self.request.get("user_comment")
		user_name = feedback.user_name

		# Notifications for a valid or invalid input.
		error = "Sorry, your input doesn't seem valid. Please try again."
		success = "Thank you so much for your feedback!"

		valid_comment = is_valid(user_comment)


		if not valid_comment:
			self.redirect("/feedback?error=%s" % error)

		else:
			post = Feedback(user_name=user_name, user_comment=user_comment)
			post.put()

			# For local development. Wait a little bit for the local Datastore to update.
			import time
			time.sleep(.1)

			query_params = {'user_name': user_name}
			self.redirect("/feedback?" + urllib.urlencode(query_params))
				   # "success=%s" % success)







app = webapp2.WSGIApplication([('/', MainPage), ('/lessonnotes', LessonNotes), ('/feedback', FeedbackPage)], debug = True) 


