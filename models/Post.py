from google.appengine.ext import db
from BlogUser import BlogUser


class Post(db.Model):
    writer = db.ReferenceProperty(BlogUser)
    title = db.StringProperty(required=True)  # note the diff: title & subject
    content = db.TextProperty(required=True)
    likes = db.IntegerProperty(default=0)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
