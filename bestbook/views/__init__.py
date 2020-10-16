#!/usr/bin/env pythonNone
#-*-coding: utf-8 -*-

"""
    __init__.py
    ~~~~~~~~~~~


    :copyright: (c) 2015 by Mek Karpeles
    :license: see LICENSE for more details.
"""

import calendar
from datetime import datetime
from flask import Flask, render_template, Response, request, session, jsonify, redirect
from flask.views import MethodView
from flask.json import JSONEncoder
from api.auth import login
from api import books
from api.books import Recommendation, Book, Request, Observation, Aspect
from api import db


PRIVATE_ENDPOINTS = []

class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                if obj.utcoffset() is not None:
                    obj = obj - obj.utcoffset()
                    millis = int(
                        calendar.timegm(obj.timetuple()) * 1000 +
                        obj.microsecond / 1000
                    )
                    return millis
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


def rest(f):
    def inner(*args, **kwargs):
        try:
            return jsonify(f(*args, **kwargs))
        except Exception as e:
            return jsonify({"error": str(e)})
        finally:
            db.rollback()
            db.remove()
    return inner


def paginate(limit=100, dump=lambda i, **opts: i.dict(**opts), **options):
    """Decorator for returning paginated json data"""
    def outer(f):
        def inner(self, cls, *args, **kwargs):
            _limit = min(int(request.args.get("limit", limit)), limit)
            _offset = int(request.args.get("page", 0)) * _limit
            verbose = bool(int(request.args.get("verbose", 0)))
            options['verbose'] = verbose
            query = f(self, cls, *args, **kwargs)
            items = query.limit(_limit).offset(_offset).all()
            # consider returning total obj count and/or current limit + page
            return {cls: [dump(i, **options) for i in items]}
        return inner
    return outer


def search(model, limit=50, lazy=True):
    query = request.args.get('query')
    field = request.args.get('field')
    limit = min(int(request.args.get('limit', limit)), limit)
    if all([query, field, limit]):
        return model.search(query, field=field, limit=limit, lazy=lazy)
    raise ValueError('Query and field must be provided. Valid fields are: %s' \
                         %  model.__table__.columns.keys())


class Base(MethodView):
    def get(self, uri="index"):
        return render_template("base.html", template="%s.html" % uri)

    
class Section(MethodView):
    def get(self, resource=""):
        if resource:
            layout = resource.replace(".html", "")
        else:
            layout = "index"
        return render_template("base.html", template="%s.html" % layout)
    
    def post(self, resource=""):
        """
        Generic POST Router which redirects /<form-component> to the right
        class (e.g. Ask, Login, Observe, Submit)
        """
        forms = {
            "ask": Ask,
            "login": Login,
            "observe": Observe,
            "submit": Submit
        }
        form = request.form
        return jsonify(forms[resource]().post())

# API POST Handlers

class Ask(MethodView):
    def post(self):
        ask = request.form
        return jsonify(ask)

class Login(MethodView):
    def post(self):
        email = request.form.get("email")
        password = request.form.get("password")
        return jsonify(login(email, password))

class Observe(MethodView):
    def post(self):
        observation = request.form
        return jsonify(observation)

class Submit(MethodView):
    def post(self):
        pass    

# API GET Router
    
class Router(MethodView):

    @rest
    def get(self, cls, _id=None):
        if not books.core.models.get(cls) or cls in PRIVATE_ENDPOINTS:
            return {"error": "Invalid endpoint"}
        if request.args.get('action') == 'search':
            return {cls: [r.dict() for r in search(books.core.models[cls])]}
        if _id:
            return books.core.models[cls].get(_id).dict(minimal=False)
        return {cls: [v.dict(minimal=True) for v in books.core.models[cls].all()]}

# Index of all available models: APIs / tables

class Index(MethodView):
    @rest
    def get(self):
        return {"endpoints": list(set(books.core.models.keys()) - set(PRIVATE_ENDPOINTS))}

# Admin Dashboard & CMS (todo: should be protected by auth)

class Admin(MethodView):
    def get(self):
        return render_template("base.html", template="admin.html", models={
            "recommendations": Recommendation,
            "books": Book,
            "requests": Request,
            "observations": Observation,
            "aspects": Aspect
        })
