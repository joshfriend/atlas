#!/usr/bin/env python

from atlas.extensions import db
from atlas.database import SurrogatePK, TimestampedModel


class SlackToken(SurrogatePK, TimestampedModel):
    token = db.Column(db.String, unique=True, nullable=False)
    channel = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

    @classmethod
    def get(cls, token):
        return cls.query.filter(cls.token == token).first()

    @classmethod
    def is_valid(cls, token):
        return cls.get(token) is not None

    def __str__(self):
        msg = '`%s`' % self.token
        if self.channel == '*':
            msg += ' in all channels: '
        else:
            msg += ' in channel #%s: ' % self.channel
        msg += self.description
        return msg
