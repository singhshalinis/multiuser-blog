from handler import Handler
from google.appengine.ext import db
from models import BlogUser
from models import Likes
from models import Post


class BlogFrontHandler(Handler):
    def render_front(self, posts, user_liked="", cookie_username=""):
        self.render("posts.html", posts=posts, user_liked=user_liked,
                    cookie_username=cookie_username)

    def get(self):
        # cookie_username = self.checkLoggedInUser()
        cookie_username = ""
        user_liked = set()

        posts = getPostsfromDataStore()
        user = self.get_curr_user()

        if user:
            cookie_username = user.username
            user_likes = getUserLikes(user.key().id())  # only those that user likes

            for ul in user_likes:
                user_liked.add(ul.postid)  # postid set for use on front end

        self.render_front(posts=posts, user_liked=user_liked,
                          cookie_username=cookie_username)


# Data store Utilities
def getPostsfromDataStore(post_id=""):
    q = db.GqlQuery("select * from Post order by created desc")
    posts = []
    for b in q.run(limit=10):
        # b.content.replace('\n', '<br>')     # convert when displaying
        posts.append(b)
    return posts


def getUser(username):
    return BlogUser.gql("where username = :1", username).get()


def getUserId(username):
    if username:
        return getUser(username).key().id()

def getUserLikes(userid):
    return Likes.gql("where userid = :1", userid)
