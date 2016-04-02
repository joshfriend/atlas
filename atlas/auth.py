#!/usr/bin/env python

from flask import g, abort, current_app as app

from atlas.extensions import auth


@auth.verify_password
def verify_login(username, password):
    g.authorized = False
    if not username == app.config['ADMIN_USERNAME']:
        return False
    if not password == app.config['ADMIN_PASSWORD']:
        return False
    g.authorized = True
    return True
