from handler import Handler

class AboutUsHandler(Handler):
    def render_front(self, cookie_username=""):
        self.render("about.html")

    def get(self):
        self.render_front()