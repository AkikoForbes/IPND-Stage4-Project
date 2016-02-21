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
	def get(self):
		# Calling data of my lesson notes from mynotes.py
		all_notes = mynotes.all_notes
		concepts_order = mynotes.concepts_order
		error = self.request.get("error", "")
		redirection = self.request.get("redirection", "")

		# Render the data into the template "lessonnotes.html"
		self.render("lessonnotes.html",
					all_notes=all_notes,
					concepts_order=concepts_order)



class FeedbackPage(Handler):
	def escape_html(s):
		return cgi.escape(s, quote = True)

	def get(self):
		# [START query]
		# Query the Datastore and order earliest date first
		feedback_query = Feedback.query().order(-Feedback.date)

		# Return a list of max 10 post objects. 
		maximum_fetch_size = 10
		feedback_list = feedback_query.fetch(maximum_fetch_size)
		# [END query]

		error = self.request.get("error", "")
		success = self.request.get("success", "")

		self.render("feedback.html",
					feedback_list=feedback_list,
					success=success,
					error=error)

	def post(self):
		user_name = self.request.get("user_name")
		user_comment = self.request.get("user_comment")

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

			self.redirect("/feedback?success=%s" % success)


def is_valid(user_input):
	if user_input.strip():
		return True
	else:
		return False




app = webapp2.WSGIApplication([('/', MainPage), ('/lessonnotes', LessonNotes), ('/feedback', FeedbackPage)], debug = True) 


