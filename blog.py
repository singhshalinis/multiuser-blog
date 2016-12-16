import os
import jinja2
import webapp2
import re
import hashlib
from datetime import datetime
from google.appengine.ext import db
import random
from string import letters


# Need it here before jinja env is set
def datetimeformat(value, format='%d/%m/%Y'):
    return value.strftime(format)

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)
jinja_env.filters['datetimeformat'] = datetimeformat

# For signup validation
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")


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


# all other handlers
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
        cookie_username = self.checkLoggedInUser()
        if cookie_username:
            self.redirect('/')  # redirect to home if already logged in
        else:
            self.render_front()

    def post(self):
        input_username = self.request.get("username")
        input_password = self.request.get("password")
        input_verify = self.request.get("verify")
        input_email = self.request.get("email")

        error = False
        username_error = password_error = verify_error = ""
        email_error = userexists_error = ""

        # user validation
        if not (valid_username(input_username)):
            username_error = "Invalid Username"
            error = True
        elif userExists(input_username) == 1:  # there is one row for this user
            userexists_error = "username already exists"
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
            secure_password = make_pw_hash(input_username, input_password)
            current_user = BlogUser(username=input_username,
                                    password=secure_password,
                                    email=input_email)
            current_user.put()      # save new user

            # login after signup
            self.setUsernameCookie(input_username)
            # self.response.headers.add_header('Set-Cookie',
            #                              str('username='
            #                              + make_secure_val(input_username)
            #                              + '; Path=/'))  # write cookie
            # redirect to Welcome page
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


# has a redirect to signin page
class SignoutHandler(Handler):
    def get(self):
        # self.response.headers.add_header('Set-Cookie',
        # str('username=;' + 'Path=/'))  # write cookie
        self.removeUsernameCookie()
        self.redirect("/signin")


# has a redirect to signin page
class WelcomeHandler(Handler):
    def render_front(self, cookie_username):
        self.render("welcome.html", cookie_username=cookie_username)

    def get(self):
        cookie_username = self.checkLoggedInUser()
        if cookie_username:
            self.render_front(cookie_username=cookie_username)
        else:
            error = "You are not signed in. Sign in to continue."
            self.redirect("/signin?error=" + str(error))  # TO-DO: Encrypt


# has a redirect to signin page
class NewpostHandler(Handler):
    def render_front(self, cookie_username, input_subject="", input_content="",
                     error=""):
        self.render("newpost.html", cookie_username=cookie_username,
                    subject=input_subject, content=input_content, error=error)

    def get(self):
        cookie_username = self.checkLoggedInUser()
        if cookie_username:
            self.render_front(cookie_username=cookie_username)
        else:
            error = "You are not signed in. Sign in to continue."
            self.redirect("/signin?error=" + str(error))  # TO-DO: Encrypt

    def post(self):
        # Check if the user is logged in and then only continue
        username = self.checkLoggedInUser()
        if not username:
            error = "You are not signed in. Sign in to continue."
            self.redirect("/signin?error=" + str(error))  # TO-DO: Encrypt

        current_user = getUser(username=username)

        # Get parameters
        input_subject = self.request.get("subject")
        input_content = self.request.get("content")

        if input_subject and input_content:
            b = Post(writer=current_user, title=input_subject,
                     content=input_content)
            b.put()
            post_id = b.key().id()

            self.redirect("/post/" + str(post_id))

        else:
            error = "Enter both, post title and post content."
            self.render_front(cookie_username=username,
                              input_subject=input_subject,
                              input_content=input_content,
                              error=error)


# Handles "home" page or default "/"
class BlogFrontHandler(Handler):
    def render_front(self, posts, user_liked="", cookie_username=""):
        self.render("posts.html", posts=posts, user_liked=user_liked,
                    cookie_username=cookie_username)

    def get(self):
        cookie_username = self.checkLoggedInUser()
        posts = getPostsfromDataStore()

        user_liked = set()
        if cookie_username:
            userid = getUserId(cookie_username)
            user_likes = getUserLikes(userid)  # only those that user likes

            for ul in user_likes:
                user_liked.add(ul.postid)  # postid set for use on front end

        self.render_front(posts=posts, user_liked=user_liked,
                          cookie_username=cookie_username)


class PermalinkHandler(Handler):
    def render_front(self, posts, cookie_username=""):
        self.render("posts.html", posts=posts, cookie_username=cookie_username)

    def get(self, post_id):
        cookie_username = self.checkLoggedInUser()
        # key = db.Key.from_path('post', int(post_id), parent=post_key())
        # post = db.get(key)
        # if not post:
        #    self.error(404)
        #    return
        if post_id:
            posts = []
            posts.append(Post.get_by_id(int(post_id)))
            if posts:
                self.render_front(posts, cookie_username=cookie_username)
            else:
                error = "Invalid request"
                self.redirect("/", error=error)
        else:
            error = "Invalid request"
            self.redirect("/", error=error)


# Handles comments
class DiscussPostHandler(Handler):
    def render_front(self, post, cookie_username=""):
        self.render("discussposts.html", post=post,
                    cookie_username=cookie_username)

    def get(self, post_id):
        cookie_username = self.checkLoggedInUser()
        post = Post.get_by_id(int(post_id))
        self.render_front(post=post, cookie_username=cookie_username)

# class CommentHandler(Handler):
#     def render_front(self, post, comments, cookie_username=""):
#         self.render("comments.html", post=post, comments = comments,
#         cookie_username=cookie_username)

#     def get(self, post_id):
#         cookie_username = self.checkLoggedInUser()
#         post = Post.get_by_id(int(post_id))
#         comments = Post.comments_set
#         self.render_front(post, comments = comments,
#         cookie_username=cookie_username)


# has a redirect to signin page
# Handles user profile
# TO-DO: This needs more feature
class ProfileHandler(Handler):
    def render_front(self, cookie_username):
        self.render("profile.html", cookie_username=cookie_username)

    def get(self):
        cookie_username = self.checkLoggedInUser()
        if cookie_username:
            self.render_front(cookie_username=cookie_username)
        else:
            error = "You are not signed in. Sign in to continue."
            self.redirect("/signin?error=" + str(error))  # TO-DO: Encrypt


# Post editing
class EditHandler(Handler):
    def render_front(self, cookie_username, postid, post, error=""):
        self.render("edit.html", cookie_username=cookie_username, post=post,
                    error=error)

    def get(self):
        cookie_username = self.checkLoggedInUser()
        if not cookie_username:
            error = "You are not signed in. Sign in to continue."
            self.redirect("/signin?error=" + str(error))  # TO-DO: Encrypt
        else:
            postid = self.request.get('postid')  # need error handling here?
            if not postid:
                self.redirect("/")
            else:
                post = Post.get_by_id(int(postid))
                self.render_front(cookie_username=cookie_username, post=post,
                                  postid=postid, error="")

    def post(self):
        # Check if the user is logged in and then only continue
        username = self.checkLoggedInUser()
        if not username:
            error = "You are not signed in. Sign in to continue."
            self.redirect("/signin?error=" + str(error))  # TO-DO: Encrypt

        # Get parameters
        input_title = self.request.get("subject")
        input_content = self.request.get("content")
        input_post_id = self.request.get("postid")
        input_post = Post.get_by_id(int(input_post_id))

        # Check for edits
        if input_post.title == input_title and input_post.content == input_content:
            error = "Nothing to update"
            self.render_front(cookie_username=username, post=input_post,
                              postid=input_post_id, error=error)
        elif input_title and input_content:
            input_post.title = input_title
            input_post.content = input_content
            k = input_post.put()
            post_id = input_post.key().id()
            self.redirect("/post/" + str(post_id))
        else:
            error = "Enter both, post title and post content."
            self.render_front(cookie_username=username, post=input_post,
                              postid=input_post_id, error=error)


# Post delete handler
class DeleteHandler(Handler):
    def post(self):

        # Check if the user is logged in and then only continue
        username = self.checkLoggedInUser()
        if not username:
            error = "You are not signed in. Sign in to continue."
            self.redirect("/signin?error=" + str(error))  # TO-DO: Encrypt

        # Get parameters
        postkey = self.request.get("postkey")
        input_post = Post.get(postkey)

        # delete
        if input_post:
            input_post.delete()
            self.redirect("/")
        else:
            error = "Cannot delete"
            self.redirect("/signup")


# user likes handler
class LikeHandler(Handler):
    def post(self):
        # Check if the user is logged in and then only continue
        username = self.checkLoggedInUser()
        if not username:
            error = "You are not signed in. Sign in to continue."
            self.redirect("/signin?error=" + str(error))  # TO-DO: Encrypt

        else:
            # Get parameters
            userid = getUserId(username)
            postid = self.request.get("postid")
            post = Post.get_by_id(int(postid))

            if getUserPostLikes(int(userid), int(postid)) == 1:
                # liked by user earlier ("getUserPostLikes" count should be 1)

                # Delete the row from Likes Entity
                likes = Likes.gql("where postid = :1 and userid = :2",
                                  int(postid), int(userid))
                for l in likes:
                    l.delete()

                # Update the Post Entity and decrease the likes
                if post.likes:
                    post.likes = post.likes - 1
                    post.put()
                # self.response.write("hello-old")

            else:  # not yet liked by user("getUserPostLikes" count 0)

                # Add a row to Likes entity
                Likes(userid=int(userid), postid=int(postid)).put()

                # Update the Post Entity and increase the likes
                if post.likes:
                    post.likes = post.likes + 1
                    post.put()
                else:
                    post.likes = 1
                    post.put()
                # self.response.write("hello-new")
            self.redirect("/")


# misc - about page handler
class AboutUsHandler(Handler):
    def render_front(self, cookie_username=""):
        self.render("about.html")

    def get(self):
        self.render_front()


# misc - contact page handler
class ContactUsHandler(Handler):
    def render_front(self, cookie_username=""):
        self.render("contactus.html")

    def get(self):
        self.render_front()


# # only for testing - delete this
# class UserHandler(Handler):
#     def get(self):
#         users = allusers()
#         self.render("allusers.html", users=users)
# # end of delete


class BlogUser(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)

    # @classmethod
    # def by_id(cls, uid):
    #     return BlogUser.get_by_id(uid, parent=users_key())

    # @classmethod
    # def by_name(cls, name):
    #     return BlogUser.all.filter('name=' + name).get()

    # @classmethod
    # def register(cls, name, pw, email):
    #     pw_hash = make_secure_val(name, pw)
    #     return BlogUser(parent=users_key(),
    #                     username=name,
    #                 password=pw_hash,
    #                 email=email)


class Post(db.Model):
    writer = db.ReferenceProperty(BlogUser)
    title = db.StringProperty(required=True)  # note the diff: title vs subject
    content = db.TextProperty(required=True)
    likes = db.IntegerProperty(default=0)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)


class Likes(db.Model):
    userid = db.IntegerProperty(required=True)
    postid = db.IntegerProperty(required=True)


# class Comments(db.Model):
#     writer = db.ReferenceProperty(BlogUser)
#     post = db.ReferenceProperty(Post)
#     text = db.TextProperty(required = True)
#     # comments = db.ReferenceProperty(Comments)
#       for handling comments on comments - TO-DO - not done yet
#     created = db.DateTimeProperty(auto_now_add = True)
#     last_modified = db.DateTimeProperty(auto_now = True)


# Misc
def getUser(username):
    return BlogUser.gql("where username = :1", username).get()


def getUserId(username):
    if username:
        return getUser(username).key().id()


# Utility Functions used on Google app engine datastore
def getPostsfromDataStore(post_id=""):
    q = db.GqlQuery("select * from Post order by created desc")
    posts = []
    for b in q.run(limit=10):
        # b.content.replace('\n', '<br>')     # convert when displaying
        posts.append(b)
    return posts


def userExists(username):
    q = db.GqlQuery("select * from BlogUser where username = :1", username)
    return q.count()


def getUserPostLikes(userid, postid):
    q = db.GqlQuery("select * from Likes where userid = :1 and postid = :2",
                    userid, postid)
    return q.count()


def getUserLikes(userid):
    return Likes.gql("where userid = :1", userid)


def allusers():
        q = db.GqlQuery("select * from BlogUser order by created")
        users = []
        for u in q.run():
            users.append(u)
        return users


# Classes, ancestors etc for Google App Engine Models
def users_key(group="default"):
    return db.Key.from_path('users', group)


def post_key(group="default"):
    return db.Key.from_path('posts', group)


def valid_signin(username, password):
    q = db.GqlQuery("select * from BlogUser where username = :1", username)
    for u in q.run():
        if valid_pw(username, password, u.password):
            return True
        else:
            return False


# Signup data validation functions

def valid_username(username):
    return USER_RE.match(username)


def valid_password(password):
    return PASSWORD_RE.match(password)


def valid_email(email):
    return EMAIL_RE.match(email)


# securing passwords, cookies using some hashing functions
def hash_str(s):
    return hashlib.md5(s).hexdigest()


def make_secure_val(s):
    return s + '|' + hash_str(s)


def check_secure_val(h):
    str = h.split('|')[0]
    if h == make_secure_val(str):
        return str


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

# end of copy
# all web handlers
app = webapp2.WSGIApplication([(r"/newpost", NewpostHandler),
                              (r"/", BlogFrontHandler),
                              (r"/post/(\d+)", PermalinkHandler),
                              (r"/signup", SignupHandler),
                              (r"/welcome", WelcomeHandler),
                              (r"/signin", SigninHandler),
                              (r"/signout", SignoutHandler),
                              (r"/profile", ProfileHandler),
                              (r"/edit", EditHandler),
                              (r"/delete", DeleteHandler),
                              (r"/like", LikeHandler),
                              (r"/discussposts/(\d+)", DiscussPostHandler),
                              (r"/about", AboutUsHandler),
                              (r"/contact", ContactUsHandler), ], debug=True)
