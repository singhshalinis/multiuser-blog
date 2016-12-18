from google.appengine.ext import db

class Likes(db.Model):
    userid = db.IntegerProperty(required=True)
    postid = db.IntegerProperty(required=True)