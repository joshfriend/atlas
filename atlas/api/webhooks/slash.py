#!/usr/bin/env python

import re
import json
from textwrap import dedent

from flask import jsonify, Response, request
from flask.views import MethodView
from webargs.flaskparser import use_args

from atlas.api import api_v1_blueprint as bp, log, require_token
from atlas.api.webhooks import slash_cmd_args
from atlas.api.webhooks.jira_mention import jira_command
from atlas.utils import slack_encode


class SlashCommand(MethodView):
    def get(self):
        # Before submitting a command to your server, Slack will occasionally
        # send your command URLs a simple GET request to verify the
        # certificate. These requests will include a parameter `ssl_check` set
        # to 1. Mostly, you may ignore these requests, but please do respond
        # with a HTTP `200 OK`.
        if request.args.get('ssl_check', 0, type=int):
            log.info('SSL Check...')
            return Response()
        else:
            abort(400)

    @require_token
    @use_args(slash_cmd_args)
    def post(self, args):
        command = args['command']
        if command == '/jira':
            return jira_command(args)
        elif command == '/debug':
            debug_data = '```\n%s\n```' % json.dumps(request.form, indent=2)
            return ephemeral_message(debug_data)
        else:
            log.error('Unknown command: %s', command)
            msg = 'I don\'t know what to do with that command :('
            return ephemeral_message(msg)


bp.add_url_rule('/webhooks/slash', view_func=SlashCommand.as_view('slash'))


def ephemeral_message(txt):
    return jsonify({
        'response_type': 'ephemeral',
        'text': slack_encode(txt),
    })
