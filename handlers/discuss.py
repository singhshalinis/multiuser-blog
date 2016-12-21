from handler import Handler
from models import Post
from error import Error_Codes
import decorator


class DiscussPostHandler(Handler):
    def render_front(self, post, cookie_username=""):
        self.render("discussposts.html", post=post,
                    cookie_username=cookie_username)

    @decorator.deco_post_exists
    def get(self, post_id):
        cookie_username = ""
        user = self.get_curr_user()
        if user:
            cookie_username = user.username
        post = Post.get_by_id(int(post_id))
        self.render_front(post=post, cookie_username=cookie_username)
