def getUser(username):
    return BlogUser.gql("where username = :1", username).get()


def getUserId(username):
    if username:
        return getUser(username).key().id()


# Utility Functions used on Google app engine datastore
def getPostsfromDataStore(post_id=""):
    q = db.GqlQuery("select * from Post order by created desc")
    posts = []
    for b in q.run(limit=10):
        # b.content.replace('\n', '<br>')     # convert when displaying
        posts.append(b)
    return posts


def userExists(username):
    q = db.GqlQuery("select * from BlogUser where username = :1", username)
    return q.count()


def getUserPostLikes(userid, postid):
    q = db.GqlQuery("select * from Likes where userid = :1 and postid = :2",
                    userid, postid)
    return q.count()


def getUserLikes(userid):
    return Likes.gql("where userid = :1", userid)


def allusers():
        q = db.GqlQuery("select * from BlogUser order by created")
        users = []
        for u in q.run():
            users.append(u)
        return users


# Classes, ancestors etc for Google App Engine Models
def users_key(group="default"):
    return db.Key.from_path('users', group)


def post_key(group="default"):
    return db.Key.from_path('posts', group)


def valid_signin(username, password):
    q = db.GqlQuery("select * from BlogUser where username = :1", username)
    for u in q.run():
        if valid_pw(username, password, u.password):
            return True
        else:
            return False

