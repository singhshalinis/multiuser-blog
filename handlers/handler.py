import jinja2
import webapp2
import os
import hashlib
from datetime import datetime

from models import BlogUser


# Need it here before jinja env is set
def datetimeformat(value, format='%d/%m/%Y'):
    return value.strftime(format)

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)
jinja_env.filters['datetimeformat'] = datetimeformat

# # error_messages (should ideally go in datastore)
# error_msg{1} = "Invalid Request"
# error_msg{2} = "Log in to continue"


# parent handler for all rendering
class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **params):
        self.write(self.render_str(template, **params))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
                     'Set-Cookie',
                     '%s=%s; Path=/' % (name, str(cookie_val)))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def get_curr_user(self):
        return self.user

    def login(self, user):
        self.set_secure_cookie('userid', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'userid=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('userid')
        self.user = uid and BlogUser.by_id(int(uid))

    def error_page(self, error_msg=""):
        """handle error pages"""
        self.redirect("/error/?error_msg=" + error_msg)



def hash_str(s):
    return hashlib.md5(s).hexdigest()


def make_secure_val(s):
    return s + '|' + hash_str(s)


def check_secure_val(h):
    str = h.split('|')[0]
    if h == make_secure_val(str):
        return str
