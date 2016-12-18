from google.appengine.ext import db

class BlogUser(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)

    # @classmethod
    # def by_id(cls, uid):
    #     return BlogUser.get_by_id(uid, parent=users_key())

    # @classmethod
    # def by_name(cls, name):
    #     return BlogUser.all.filter('name=' + name).get()

    # @classmethod
    # def register(cls, name, pw, email):
    #     pw_hash = make_secure_val(name, pw)
    #     return BlogUser(parent=users_key(),
    #                     username=name,
    #                 password=pw_hash,
    #                 email=email)