from models import BlogUser
from models import Likes
from models import Post
from error import Error_Codes

# all decorators
def deco_post_exists(func):
    def g(hand, postid, *args, **kwargs):
        if Post.get_by_id(int(postid)):
            return func(hand, postid, *args, **kwargs)
        else:
            # return hand.error_page(Error_Codes.POST_DOES_NOT_EXIST)
            return hand.error_page()
    return g

def deco_user_owns_post(func):
    def g(hand, postid="", *args, **kwargs):
        pid = hand.request.get("postid")
        if pid:
            post = Post.get_by_id(int(pid))
            if post.writer.username == hand.get_curr_user().username:
                func(hand, *args, **kwargs)
            else:
                return hand.error_page()
        else:
            return hand.error_page()
    return g

def deco_user_owns_and_post_exists(func):
    def g(hand, postid, *args, **kwargs):
        post = Post.get_by_id(int(postid))
        if post:
            if post.writer.username == hand.get_curr_user().username:
                return func(hand, postid, *args, **kwargs)
            else:
                return hand.error_page()
        else:
            # return hand.error_page(Error_Codes.POST_DOES_NOT_EXIST)
            return hand.error_page()
    return g


def deco_user_not_owns_post(func):
    def g(hand, postid="", *args, **kwargs):
        pid = hand.request.get("postid")
        if pid:
            post = Post.get_by_id(int(pid))
            if post.writer.username == hand.get_curr_user().username:
                 return hand.error_page()
            else:
                func(hand, *args, **kwargs)
        else:
            return hand.error_page()
    return g



def check_user_exists(userid):
    return User.get_by_id(userid)

# def user_owns_comments():
# comments is powered by DISQUS and is not in scope here
