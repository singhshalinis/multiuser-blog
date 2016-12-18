import hashlib
import random

from handler import Handler
from google.appengine.ext import db
from string import letters


# from models import BlogUser
# from models import Likes
# from models import Post

class SigninHandler(Handler):
    def render_front(self, error="", input_username="", input_password="",
                     username_error="", password_error="", signin_error=""):
        self.render("signin.html", error=error,
                    input_username=input_username,
                    input_password=input_password,
                    signin_error=signin_error,
                    username_error=username_error,
                    password_error=password_error)

    def get(self, error=""):
        cookie_username = self.checkLoggedInUser()
        if cookie_username:
            self.redirect('/')
        else:
            error = self.request.get("error")
            self.render_front(error=error)

    def post(self):
        username_error = password_error = signin_error = ""
        error = False

        input_username = self.request.get('username')
        input_password = self.request.get('password')

        if not input_username:
            username_error = "Please enter username"
            error = True

        if not input_password:
            password_error = "Please enter password"
            error = True

        if not error:
            # login (or signin)
            if valid_signin(input_username, input_password):
                # self.response.headers.add_header('Set-Cookie',
                #     str('username=' + make_secure_val(input_username)
                #     + '; Path=/'))  # write cookie
                self.setUsernameCookie(input_username)
                self.redirect("/welcome")
            else:
                signin_error = "Invalid username or password"
                error = True

        if error:
            # self.response.headers.add_header('Set-Cookie', None)
            self.removeUsernameCookie()
            self.render_front(input_username=input_username,
                              input_password=input_password,
                              signin_error=signin_error,
                              username_error=username_error,
                              password_error=password_error)

def valid_signin(username, password):
    q = db.GqlQuery("select * from BlogUser where username = :1", username)
    for u in q.run():
        if valid_pw(username, password, u.password):
            return True
        else:
            return False


# got from hw4
def make_salt(length=5):
    return ''.join(random.choice(letters) for x in xrange(length))


def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)


def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

