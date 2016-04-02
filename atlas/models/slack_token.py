#!/usr/bin/env python

from atlas.extensions import db
from atlas.database import SurrogatePK, TimestampedModel


class SlackToken(SurrogatePK, TimestampedModel):
    token = db.Column(db.String, unique=True, nullable=False)
    room = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

    @classmethod
    def is_valid(cls, token):
        t = cls.query.filter(cls.token == token).first()
        return t is not None
