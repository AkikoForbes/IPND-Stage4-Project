# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

# All the data of my notes in a python file
import mynotes


# Specify a path to a template directry
template_dir = os.path.join(os.path.dirname(__file__), "html_templates")
# Set up a jinja environment
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               extensions=["jinja2.ext.autoescape"],
                               autoescape = True)
# [END imports]


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
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    datetime = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(Handler):

    def get(self):
        self.render("index.html")


class UnitOne(Handler):

    def get(self):
        # Calling data of my lesson notes from mynotes.py
        unit = mynotes.unit1
        concepts_order = mynotes.concepts_order

        # Render the data into the template "unitone.html"
        self.render("unitone.html",
                    unit=unit,
                    concepts_order=concepts_order)


class UnitTwo(Handler):

    def get(self):
        unit = mynotes.unit2
        concepts_order = mynotes.concepts_order

        self.render("unittwo.html",
                    unit=unit,
                    concepts_order=concepts_order)


class UnitThree(Handler):

    def get(self):
        unit = mynotes.unit3
        concepts_order = mynotes.concepts_order

        self.render("unitthree.html",
                    unit=unit,
                    concepts_order=concepts_order)


class UnitFour(Handler):

    def get(self):
        unit = mynotes.unit4
        concepts_order = mynotes.concepts_order

        self.render("unitfour.html",
                    unit=unit,
                    concepts_order=concepts_order)


class UnitFive(Handler):

    def get(self):
        unit = mynotes.unit5
        concepts_order = mynotes.concepts_order

        self.render("unitfive.html",
                    unit=unit,
                    concepts_order=concepts_order)


class UnitSix(Handler):

    def get(self):
        unit = mynotes.unit6
        concepts_order = mynotes.concepts_order

        self.render("unitsix.html",
                    unit=unit,
                    concepts_order=concepts_order)


class UnitSeven(Handler):

    def get(self):
        unit = mynotes.unit7
        concepts_order = mynotes.concepts_order

        self.render("unitseven.html",
                    unit=unit,
                    concepts_order=concepts_order)


class UnitEight(Handler):

    def get(self):
        unit = mynotes.unit8
        concepts_order = mynotes.concepts_order

        self.render("uniteight.html",
                    unit=unit,
                    concepts_order=concepts_order)


def is_valid(user_input):
    if user_input.strip():
        return True
    else:
        return False


class FeedbackPage(Handler):

    def get(self):
        feedback_name = self.request.get('feedback_name', DEFAULT_FEEDBACK_NAME)

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


class Guestbook(Handler):

    def post(self):

        feedback_name = self.request.get('feedback_name', DEFAULT_FEEDBACK_NAME)
        feedback = Feedback(parent=feedback_key(feedback_name))

        if users.get_current_user():
            feedback.author = Author(
                identity=users.get_current_user().user_id(),
                email=users.get_current_user().email())

        # Notifications for a valid or invalid input.
        error = "Sorry, your input doesn't seem valid. Please try again."
        success = "Thank you so much for your feedback!"

        # Validate user content
        feedback.content = self.request.get("content")
        valid_content = is_valid(feedback.content)


        if not valid_content:
            self.redirect("/feedback?error=%s" % error)

        else:
            feedback.put()

            query_params = {'feedback_name': feedback_name}
            self.redirect("/feedback?" + urllib.urlencode(query_params) +"&success=%s" % success)


app = webapp2.WSGIApplication([('/', MainPage), ('/unitone', UnitOne), ('/unittwo', UnitTwo),
                               ('/unitthree', UnitThree), ('/unitfour', UnitFour), ('/unitfive', UnitFive),
                               ('/unitsix', UnitSix), ('/unitseven', UnitSeven), ('/uniteight', UnitEight),
                               ('/feedback', FeedbackPage), ('/sign', Guestbook)], debug = True)

