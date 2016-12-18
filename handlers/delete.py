from handler import Handler
from models import Post

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
