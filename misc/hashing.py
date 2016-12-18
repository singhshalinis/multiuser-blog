# securing passwords, cookies using some hashing functions
def hash_str(s):
    return hashlib.md5(s).hexdigest()


def make_secure_val(s):
    return s + '|' + hash_str(s)


def check_secure_val(h):
    str = h.split('|')[0]
    if h == make_secure_val(str):
        return str


# got from hw4
def make_salt(length=5):
    return ''.join(random.choice(letters) for x in xrange(length))


def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)


def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)
