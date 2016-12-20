from google.appengine.ext import db

class BlogUser(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)

    @classmethod
    def by_id(cls, uid):
        return BlogUser.get_by_id(uid)

    @classmethod
    def validateUserid(userid):
        if userid:
            user = BlogUser.by_id(cookie_userid)
            if user:
                return user