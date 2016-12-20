import jinja2
import webapp2
from datetime import datetime
from google.appengine.ext import db
import random
from string import letters

from models import BlogUser
from models import Likes
from models import Post

from handlers import NewpostHandler
from handlers import AboutUsHandler
from handlers import ContactUsHandler
from handlers import DeleteHandler
from handlers import DiscussPostHandler
from handlers import SignupHandler
from handlers import BlogFrontHandler
from handlers import EditHandler
from handlers import LikeHandler
from handlers import NewpostHandler
from handlers import PermalinkHandler
from handlers import ProfileHandler
from handlers import SigninHandler
from handlers import SignoutHandler
from handlers import WelcomeHandler
from handlers import ErrorHandler


# all web handlers
app = webapp2.WSGIApplication([(r"/newpost", NewpostHandler),
                              (r"/", BlogFrontHandler),
                              (r"/post/(\d+)", PermalinkHandler),
                              (r"/signup", SignupHandler),
                              (r"/welcome", WelcomeHandler),
                              (r"/signin", SigninHandler),
                              (r"/signout", SignoutHandler),
                              (r"/profile", ProfileHandler),
                              (r"/edit/(\d+)", EditHandler),
                              (r"/delete", DeleteHandler),
                              (r"/like", LikeHandler),
                              (r"/discussposts/(\d+)", DiscussPostHandler),
                              (r"/about", AboutUsHandler),
                              #  (r"/error/([0-9]+)", ErrorHandler), #TBD
                              (r"/error", ErrorHandler),
                              (r"/contact", ContactUsHandler), ], debug=True)
