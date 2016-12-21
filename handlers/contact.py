from handler import Handler


class ContactUsHandler(Handler):
    def render_front(self, cookie_username=""):
        self.render("contactus.html")

    def get(self):
        self.render_front()
