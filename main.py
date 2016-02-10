import cgi
# import urllib
import webapp2
import jinja2
import os

# from google.appengine.api import users
from google.appengine.ext import ndb

# All the data of my notes in a python file 
import mynotes


# Specify a path to a template directry
template_dir = os.path.join(os.path.dirname(__file__), "html_templates")
# Set up a jinja environment
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
							   extensions=["jinja2.ext.autoescape"],
							   autoescape = True)


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


class Feedback(ndb.Model):
	"""A main model for representing an individual Guestbook entry."""
	user_name = ndb.StringProperty()
	user_comment = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(Handler):
	def get(self):
		self.render("index.html")


class LessonNotes(Handler):
	def escape_html(s):
		return cgi.escape(s, quote = True)

	def get(self):
		# Calling data of my lesson notes from mynotes.py
		all_notes = mynotes.all_notes
		concepts_order = mynotes.concepts_order
		notification = ""

		# Render the data into the template "lessonnotes.html"
		self.render("lessonnotes.html",
					all_notes=all_notes,
					concepts_order=concepts_order,
					notification=notification)

	def post(self):
		user_name = self.request.get("user_name")
		user_comment = self.request.get("user_comment")

		# If there's invalid user input, error message will show up.
		error = "Sorry, your input doesn't seem valid. Please make sure to fill in both comment and name sections."


		if not is_valid(user_comment):
			self.redirect("/lessonnotes?notification=%s" % error)

		else:
			self.redirect("/feedback")

	def is_valid(user_input):
		blanks = user_input.isspace()
		if blanks:
			return user_input



class FeedbackPage(Handler):
	def get(self):
		# [START query]
		# Query the Datastore and order earliest date first
		feedback_query = Feedback.query().order(-Feedback.date)

		# Return a list of max 10 post objects. 
		maximum_fetch_size = 10
		feedback_list = feedback_query.fetch(maximum_fetch_size)
		# [END query]

		notification = self.request.get("notification", "")

		self.render("feedback.html",
					feedback_list=feedback_list,
					notification=notification)

	def post(self):
		user_name = self.request.get("user_name")
		user_comment = self.request.get("user_comment")

		#success message text for notification
		success = "Thank you for your feedback!"

		post = Feedback(user_name=user_name, user_comment=user_comment)
		post.put()

		# For local development. Wait a little bit for the local Datastore to update.
		import time
		time.sleep(.1)

		self.redirect("/feedback?notification=%s" % success)



app = webapp2.WSGIApplication([('/', MainPage), ('/lessonnotes', LessonNotes), ('/feedback', FeedbackPage)], debug = True) 


