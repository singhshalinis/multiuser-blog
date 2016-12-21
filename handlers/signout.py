from handler import Handler


class SignoutHandler(Handler):
    def get(self):
        self.logout()
        self.redirect("/signin")
