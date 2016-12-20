from handler import Handler
from models import Post

import decorator

class DeleteHandler(Handler):


    @decorator.deco_user_owns_post
    def post(self):
        cookie_username = ""
        user = self.get_curr_user()
        if user:
            cookie_username = user.username
        else:
            error = "You are not signed in. Sign in to continue."
            self.redirect("/signin?error=" + str(error))  # TO-DO: Encrypt

        # Get parameters
        postid = self.request.get("postid")
        input_post = Post.get_by_id(int(postid))

        # delete
        if input_post:
            input_post.delete()
            self.redirect("/")
        else:
            error = "Cannot delete"
            self.redirect("/signup")
