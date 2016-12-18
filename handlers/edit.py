from handler import Handler
from google.appengine.ext import db
from models import BlogUser
from models import Likes
from models import Post

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
