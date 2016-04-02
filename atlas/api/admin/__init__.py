#!/usr/bin/env python

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from atlas.extensions import db
from atlas.models import SlackToken

admin = Admin(name='Atlas', template_mode='bootstrap3')


class TokenModelView(ModelView):
    form_excluded_columns = [
        'created_at',
        'last_updated',
    ]

admin.add_view(TokenModelView(SlackToken, db.session))
