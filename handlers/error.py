from handler import Handler

class Error_Codes:
    POST_DOES_NOT_EXIST = 1
    NOT_OWNER = 2

# TO-DO: Error codes are not being used yet.
# Implement the error codes (is it needed?)
class ErrorHandler(Handler):
    def render_front(self, error=""):
        self.render("error.html", error=error)

    def get(self, error_cd=""):
        error = "Invalid Request"

        # not being used in this version
        if error_cd:
            error = "Invalid Request: "
            err_cd = int(error_cd)
            if err_cd == Error_Codes.POST_DOES_NOT_EXIST:
                error += "Post does not exist"
            elif err_cd == Error_Codes.NOT_OWNER:
                error += "User does not own this post"

        self.render_front(error=error)