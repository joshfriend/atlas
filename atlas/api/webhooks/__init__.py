#!/usr/bin/env python

import logging

from webargs import fields

log = logging.getLogger('api.webhook')


webhook_args = {
    'token': fields.Str(required=True),
    'team_id': fields.Str(),
    'team_domain': fields.Str(),
    'channel_id': fields.Str(required=True),
    'channel_name': fields.Str(required=True),
    'timestamp': fields.Float(),
    'user_id': fields.Str(),
    'user_name': fields.Str(required=True),
    'text': fields.Str(required=True),
    'trigger_word': fields.Str(),
}

slash_cmd_args = {
    'token': fields.Str(required=True),
    'team_id': fields.Str(),
    'team_domain': fields.Str(),
    'channel_id': fields.Str(required=True),
    'channel_name': fields.Str(required=True),
    'user_id': fields.Str(),
    'user_name': fields.Str(required=True),
    'text': fields.Str(required=True),
    'response_url': fields.Str(),
    'command': fields.Str(required=True),
}
