#!/usr/bin/env python

from flask import jsonify, Response
from flask.views import MethodView
from webargs.flaskparser import use_args

from atlas.api import api_v1_blueprint as bp, log
from atlas.api.webhooks import slash_cmd_args
from atlas.api.webhooks.jira_mention import jira_command


class SlashCommand(MethodView):
    def get(self):
        # Before submitting a command to your server, Slack will occasionally
        # send your command URLs a simple GET request to verify the
        # certificate. These requests will include a parameter `ssl_check` set
        # to 1. Mostly, you may ignore these requests, but please do respond
        # with a HTTP `200 OK`.
        return Response()

    @use_args(slash_cmd_args)
    def post(self, args):
        command = args['command']
        if command == 'jira':
            return jira_command(args)
        else:
            log.error('Unknown command: /%s', command)
            return jsonify({
                "response_type": "ephemeral",
                "text": "I don't know what to do with that command :(",
            })


bp.add_url_rule('/webhooks/slash', view_func=SlashCommand.as_view('slash'))
