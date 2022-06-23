#!/usr/bin/env python3

"""
    __init__.py
    ~~~~~~~~~~~


    :copyright: (c) 2022 by OBGP Team
    :license: AGPL, see LICENSE for more details.
"""

import os
import types
from configparser import ConfigParser

path = os.path.dirname(os.path.realpath(__file__))
approot = os.path.abspath(os.path.join(path, os.pardir))


def getdef(self, section, option, default_value):
    try:
        return self.get(section, option)
    except Exception:
        return default_value

config = ConfigParser()
config.read('%s/secrets.cfg' % path)
config.getdef = types.MethodType(getdef, config)

SECRET_KEY = config.getdef('app', 'secret_key', 'insecure')

HOST = config.getdef("app", "host", '0.0.0.0')
PORT = int(config.getdef("app", "port", 5000))
DEBUG = bool(int(config.getdef("app", "debug", 0)))
OPTIONS = {'debug': DEBUG, 'host': HOST, 'port': PORT}
