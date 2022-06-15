
from flask.views import MethodView

class Login(MethodView):
    def get(self):
        return "Welcome to login"

    def post(self):
        r = request.args
        return r
