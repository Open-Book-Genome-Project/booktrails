
from flask import render_template
from flask.views import MethodView
from . import auth

class Home(MethodView):
    def get(self):
        return render_template(
            "base.html",
            template="index.html",
            app_name="BookTrails"
        )
