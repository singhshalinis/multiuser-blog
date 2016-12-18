from handler import Handler
from models import Post

class DiscussPostHandler(Handler):
    def render_front(self, post, cookie_username=""):
        self.render("discussposts.html", post=post,
                    cookie_username=cookie_username)

    def get(self, post_id):
        cookie_username = self.checkLoggedInUser()
        post = Post.get_by_id(int(post_id))
        self.render_front(post=post, cookie_username=cookie_username)
