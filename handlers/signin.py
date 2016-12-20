from handler import Handler
from google.appengine.ext import db


# local module
import utilities

from models import BlogUser
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
        # if user is already logged in - redirect to home page
        user = self.get_curr_user()
        if user:
            self.redirect('/')
        else:
            error = self.request.get("error")  # if an error was passed
            self.render_front(error=error)

    def post(self):
        username_error = password_error = signin_error = ""
        error = False

        # get parameters
        input_username = self.request.get('username')
        input_password = self.request.get('password')

        # validate
        if not input_username:
            username_error = "Please enter username"
            error = True

        if not input_password:
            password_error = "Please enter password"
            error = True

        if not error:
            # login (or signin) if no error
            user = valid_signin(input_username, input_password)
            if user:
                self.login(user)
                self.redirect("/welcome")
            else:
                signin_error = "Invalid username or password"
                error = True

        if error:
            self.render_front(input_username=input_username,
                              input_password=input_password,
                              signin_error=signin_error,
                              username_error=username_error,
                              password_error=password_error)

# validate username - password
def valid_signin(username, password):
    u = BlogUser.gql("where username = :1", username).get()
    if valid_pw(username, password, u.password):
        return u

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == utilities.make_pw_hash(name, password, salt)
