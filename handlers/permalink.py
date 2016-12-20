from handler import Handler
from models import Post

import decorator

class PermalinkHandler(Handler):
    def render_front(self, posts, cookie_username=""):
        self.render("posts.html", posts=posts, cookie_username=cookie_username)

    @decorator.deco_post_exists
    def get(self, post_id):

        cookie_username = ""
        user = self.get_curr_user()
        if user:
            cookie_username = user.username

        posts = []
        posts.append(Post.get_by_id(int(post_id)))
        self.render_front(posts, cookie_username=cookie_username)
