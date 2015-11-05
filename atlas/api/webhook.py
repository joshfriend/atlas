#!/usr/bin/env python

import re
import os
import logging
import textwrap

from flask import request, Response, current_app, abort, request, jsonify
from webargs import fields
from webargs.flaskparser import use_args
from jira import JIRA

from atlas.api import api_v1_blueprint as bp

log = logging.getLogger('api.webhook')

jira_key_re = re.compile(r'[A-Z]+-\d+')

webhook_args = {
    'token': fields.Str(required=True),
    'team_id': fields.Str(),
    'team_domain': fields.Str(),
    'channel_id': fields.Str(),
    'channel_name': fields.Str(required=True),
    'timestamp': fields.Float(),
    'user_id': fields.Str(),
    'user_name': fields.Str(required=True),
    'text': fields.Str(required=True),
    'trigger_word': fields.Str(),
}


@bp.route('/webhooks/jira', methods=['POST'])
@use_args(webhook_args)
def on_msg(args):
    if args['token'] not in current_app.config['SLACK_WEBHOOK_TOKENS']:
        log.warning('Invalid token: %s', args['token'])
        abort(401)

    if args['user_name'] == current_app.config['SLACK_WEBHOOK_USERNAME']:
        # Avoid infinite feedback loop of bot parsing it's own messages :)
        return Response()

    match = jira_key_re.search(args['text'])
    if match:
        issue_key = match.group(0)
        log.info('Message contained JIRA issue key: %s', issue_key)

        # Login to JIRA
        authinfo = (
            current_app.config['JIRA_USERNAME'],
            current_app.config['JIRA_PASSWORD'],
        )
        jira_url = current_app.config['JIRA_URL']
        jira = JIRA(jira_url, basic_auth=authinfo)

        # Retrieve issue
        issue = jira.issue(issue_key)
        if issue:
            return jsonify({
                'text': get_formatted_issue_message(issue),
            })

    return Response()


def get_formatted_issue_message(issue):
    message = textwrap.dedent("""\
    *{issue.key}:* {issue.fields.summary}
    `{issue.fields.issuetype.name}` - `{issue.fields.priority.name}` - `{issue.fields.status.name}`
    """.format(issue=issue))
    if issue.fields.assignee:
        message += textwrap.dedent("""\
        Assigned to: {issue.fields.assignee.displayName}
        """.format(issue=issue))
    message += os.path.join(
        current_app.config['JIRA_URL'],
        'browse',
        issue.key
    )
    message = message.rstrip('\n')
    return message
