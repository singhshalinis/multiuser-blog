from handler import Handler



# TO-DO: Error codes are not being used yet.
# Implement the error codes (is it needed?)
error_codes = {}
error_codes{'POST_DOES_NOT_EXIST'} = "The post does not exist"
error_codes{'NOT_OWNER'} = "Is not the owner"
error_codes{'NOT_SIGNED_IN'} = "User is not signed in"


class ErrorHandler(Handler):
    def render_front(self, error=""):
        self.render("error.html", error=error)

    def get(self):
        error_msg = self.request.get("error_msg")
        error = "Invalid Request: " + error_msg
        self.render_front(error=error)
