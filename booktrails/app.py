#!/usr/bin/env python
#-*-coding: utf-8 -*-

"""
    app.py
    ~~~~~~

    :copyright: (c) 2022 Open Book Genome Project
    :license: BSD, see LICENSE for more details.
"""

from flask import Flask, render_template
from flask.views import MethodView
from flask_routing import router
from flask_cors import CORS
from views.auth import Login

class Home(MethodView):
    def get(self):
        return render_template("index.html", app_name="BookTrails")
    
urls = (
    '/', Home,
    '/login', Login,
)

app = router(Flask(__name__), urls)

if __name__ == "__main__":
    app.run()

