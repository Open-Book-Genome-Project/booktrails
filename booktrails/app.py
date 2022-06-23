#!/usr/bin/env python
#-*-coding: utf-8 -*-

"""
    app.py
    ~~~~~~

    :copyright: (c) 2022 Open Book Genome Project
    :license: AGPL3, see LICENSE for more details.
"""

from flask import Flask, render_template
from flask.views import MethodView
from flask_routing import router
from configs import SECRET_KEY, OPTIONS
import views
    
urls = (
    '/', views.Home,
    '/login', views.auth.Login,
)

app = router(Flask(__name__), urls)
app.secret_key = SECRET_KEY

if __name__ == "__main__":
    app.run(**OPTIONS)
