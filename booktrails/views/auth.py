
from flask import render_template, request, redirect
from flask.views import MethodView
from api.auth import login

class Login(MethodView):
    def get(self):
        return render_template("base.html", template="login.html")

    def post(self):
        email = request.form.get("email")
        password = request.form.get("password")
        if login(email, password):
            return redirect('/')
        else:
            return "login failed"


class Logout(MethodView):
    def get(self):
        session.pop('username', '')
        return redirect('/')
