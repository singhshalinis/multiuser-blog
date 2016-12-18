from handler import Handler
from models import BlogUser
from models import Post

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

def getUser(username):
    return BlogUser.gql("where username = :1", username).get()


def getUserId(username):
    if username:
        return getUser(username).key().id()