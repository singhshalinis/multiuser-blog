import jinja2
import webapp2
import os
import hashlib
from datetime import datetime




# Need it here before jinja env is set
def datetimeformat(value, format='%d/%m/%Y'):
    return value.strftime(format)

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)
jinja_env.filters['datetimeformat'] = datetimeformat


# parent handler for all rendering
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **params):
        self.write(self.render_str(template, **params))

    def setUsernameCookie(self, name):
        secure_pwd = make_secure_val(name)
        self.response.headers.add_header(
                     'Set-Cookie',
                     'username=%s; Path=/' % (str(name)))

    def removeUsernameCookie(self):
        self.response.headers.add_header('Set-Cookie', 'username=; Path=/')

    def checkLoggedInUser(self):
        cookie_username = ""
        usrnm = self.request.cookies.get('username')
        if usrnm:
            cookie_username = usrnm.split('|')[0]
        return cookie_username

def make_secure_val(s):
    return s + '|' + hash_str(s)

def hash_str(s):
    return hashlib.md5(s).hexdigest()

