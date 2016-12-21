from models import BlogUser
from models import Likes
from models import Post
from error import Error_Codes


# newpost, edit, delete, like
def deco_user_signed_in(func):
    def g(hand, *args, **kwargs):
        user = hand.get_curr_user()
        if user:
            func(hand, *args, **kwargs)
        else:
            error = "You are not signed in. Sign in to continue."
            hand.redirect("/signin?error=" + str(error))
    return g


def deco_post_exists(func):
    def g(hand, postid, *args, **kwargs):
        if Post.get_by_id(int(postid)):
            return func(hand, postid, *args, **kwargs)
        else:
            error_msg = "The post does not exist"
            hand.error_page(error_msg)
    return g


# used for edit
def deco_user_owns_and_post_exists(func):
    def g(hand, postid, *args, **kwargs):
        post = Post.get_by_id(int(postid))
        if post:
            if post.writer.username == hand.get_curr_user().username:
                return func(hand, postid, *args, **kwargs)
            else:
                error_msg = "User does not own this post!"
                hand.error_page(error_msg)
        else:
            error_msg = "The post does not exist"
            hand.error_page(error_msg)
    return g


# used for delete - similar to edit, except postid is available as a parameter
def deco_user_owns_and_post_exists_del(func):
    def g(hand, *args, **kwargs):
        postid = hand.request.get("postid")
        post = Post.get_by_id(int(postid))
        if post:
            if post.writer.username == hand.get_curr_user().username:
                return func(hand, *args, **kwargs)
            else:
                error_msg = "User does not own this post!"
                hand.error_page(error_msg)
        else:
            error_msg = "The post does not exist"
            hand.error_page(error_msg)
    return g


# used in like
def deco_user_not_owns_post_exists(func):
    def g(hand, postid="", *args, **kwargs):
        pid = hand.request.get("postid")
        if pid:
            post = Post.get_by_id(int(pid))
            if post.writer.username == hand.get_curr_user().username:
                error_msg = "Cannot like your own post!"
                hand.error_page(error_msg)
            else:
                func(hand, *args, **kwargs)
        else:
            error_msg = "The post does not exist"
            hand.error_page(error_msg)
    return g

# def user_owns_comments():
# comments is powered by DISQUS and is not in scope here

#
# def deco_user_owns_post(func):
#     def g(hand, postid="", *args, **kwargs):
#         pid = hand.request.get("postid")
#         if pid:
#             post = Post.get_by_id(int(pid))
#             if post.writer.username == hand.get_curr_user().username:
#                 func(hand, *args, **kwargs)
#             else:
#                 return hand.error_page()
#         else:
#             return hand.error_page()
#     return g

