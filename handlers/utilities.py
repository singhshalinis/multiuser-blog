import hashlib
import random

from string import letters

# got from hw4
def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)


def make_salt(length=5):
    return ''.join(random.choice(letters) for x in xrange(length))
