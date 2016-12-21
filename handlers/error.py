from handler import Handler


# TO-DO: Error codes are not being used yet.
# Implement the error codes (is it needed?)
class Error_Codes:
    POST_DOES_NOT_EXIST = 1
    NOT_OWNER = 2


class ErrorHandler(Handler):
    def render_front(self, error=""):
        self.render("error.html", error=error)

    def get(self):
        error_msg = self.request.get("error_msg")
        error = "Invalid Request: " + error_msg
        self.render_front(error=error)
