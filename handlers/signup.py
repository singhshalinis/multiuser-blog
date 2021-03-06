import re

from google.appengine.ext import db
from handler import Handler
from models import BlogUser

import utilities


class SignupHandler(Handler):
    def render_front(self, input_username="", input_password="",
                     input_verify="", input_email="", username_error="",
                     password_error="", verify_error="", email_error="",
                     userexists_error=""):
        self.render("signup.html", input_username=input_username,
                    input_password=input_password,
                    input_verify=input_verify,
                    input_email=input_email,
                    username_error=username_error,
                    password_error=password_error,
                    verify_error=verify_error,
                    email_error=email_error,
                    userexists_error=userexists_error)

    def get(self):
        # if user is already logged in - redirect to home page
        user = self.get_curr_user()
        if user:
            self.redirect('/')
        else:
            self.render_front()

    def post(self):
        error = False
        username_error = password_error = verify_error = ""
        email_error = userexists_error = ""

        # get parameters
        input_username = self.request.get("username")
        input_password = self.request.get("password")
        input_verify = self.request.get("verify")
        input_email = self.request.get("email")

        # username validation
        if not input_username:
            username_error = "No username provided"
            error = True
        elif not (valid_username(input_username)):
            username_error = "Invalid Username"
            error = True
        elif userExists(input_username) == 1:  # there is 1 row for this user
            userexists_error = "Username already exists"
            error = True

        # password validation
        if not input_password:
            password_error = "No password provided"
            input_verify = ""
            error = True
        elif not (valid_password(input_password)):
            password_error = "Invalid Password"
            input_verify = ""
            error = True
        elif input_password != input_verify:
            verify_error = "Passwords don't match"
            error = True

        # email validation
        if input_email:
            if not (valid_email(input_email)):
                email_error = "Invalid Email"
                error = True

        if not error:
            secure_password = utilities.make_pw_hash(input_username, input_password)
            current_user = BlogUser(username=input_username,
                                    password=secure_password,
                                    email=input_email)
            current_user.put()      # save new user

            # login after signup
            self.login(current_user)
            self.redirect("/welcome")

        else:
        # error
            self.render_front(input_username=input_username,
                              input_password=input_password,
                              input_verify=input_verify,
                              input_email=input_email,
                              username_error=username_error,
                              password_error=password_error,
                              verify_error=verify_error,
                              email_error=email_error,
                              userexists_error=userexists_error)


# Signup data validation functions
def valid_username(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return USER_RE.match(username)


def valid_password(password):
    PASSWORD_RE = re.compile(r"^.{3,20}$")
    return PASSWORD_RE.match(password)


def valid_email(email):
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
    return EMAIL_RE.match(email)


def userExists(username):
    q = db.GqlQuery("select * from BlogUser where username = :1", username)
    return q.count()