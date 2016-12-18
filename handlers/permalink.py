from handler import Handler
from models import Post

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
