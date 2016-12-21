from handler import Handler


# TO-DO: This needs more feature
class ProfileHandler(Handler):
    def render_front(self, cookie_username):
        self.render("profile.html", cookie_username=cookie_username)

    def get(self):
        cookie_username = ""
        user = self.get_curr_user()
        if user:
            cookie_username = user.username

        if cookie_username:
            self.render_front(cookie_username=cookie_username)
        else:
            error = "You are not signed in. Sign in to continue."
            self.redirect("/signin?error=" + str(error))  # TO-DO: Encrypt
