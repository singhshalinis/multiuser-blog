from handler import Handler

class SignoutHandler(Handler):
    def get(self):
        # self.response.headers.add_header('Set-Cookie',
        # str('username=;' + 'Path=/'))  # write cookie
        self.removeUsernameCookie()
        self.redirect("/signin")

