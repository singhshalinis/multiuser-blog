from handler import Handler

class WelcomeHandler(Handler):
    def render_front(self, cookie_username):
        self.render("welcome.html", cookie_username=cookie_username)

    def get(self):
        user = self.get_curr_user()
        if user:
            self.render_front(cookie_username=user.username)
        else:
            error = "You are not signed in. Sign in to continue."
            self.redirect("/signin?error=" + str(error))  # TO-DO: Encrypt

