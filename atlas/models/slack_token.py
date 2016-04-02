#!/usr/bin/env python

from sqlalchemy import and_

from atlas.extensions import db
from atlas.database import SurrogatePK, TimestampedModel


class SlackToken(SurrogatePK, TimestampedModel):
    token = db.Column(db.String, unique=True, nullable=False)
    room = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

    @classmethod
    def is_valid(cls, token, room=None):
        conditions = [
            cls.token == token,
        ]
        if room:
            conditions.append(cls.room == room)
        t = cls.query.filter(and_(*conditions)).first()
        return t is not None
