from google.appengine.ext import db

from handler import Handler
from models import BlogUser
from models import Post
from models import Likes

import decorator

class LikeHandler(Handler):

    @decorator.deco_user_not_owns_post
    def post(self):
        cookie_username = ""
        user = self.get_curr_user()
        if not user:
            error = "You are not signed in. Sign in to continue."
            self.redirect("/signin?error=" + str(error))  # TO-DO: Encrypt
        else:
            cookie_username = user.username
            postid = self.request.get("postid")
            post = Post.get_by_id(int(postid))
            userid = user.key().id()

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
            self.redirect("/")

def getUserPostLikes(userid, postid):
    q = db.GqlQuery("select * from Likes where userid = :1 and postid = :2",
                    userid, postid)
    return q.count()