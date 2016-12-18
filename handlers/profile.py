from handler import Handler

# TO-DO: This needs more feature
class ProfileHandler(Handler):
    def render_front(self, cookie_username):
        self.render("profile.html", cookie_username=cookie_username)

    def get(self):
        cookie_username = self.checkLoggedInUser()
        if cookie_username:
            self.render_front(cookie_username=cookie_username)
        else:
            error = "You are not signed in. Sign in to continue."
            self.redirect("/signin?error=" + str(error))  # TO-DO: Encrypt
