#!/usr/bin/env python

import re
import os
import time
import logging
from datetime import datetime

from flask import request, Response, current_app, abort, request, jsonify
from webargs import fields
from webargs.flaskparser import use_args
from jira import JIRA, JIRAError

from atlas.api import api_v1_blueprint as bp
from atlas.extensions import redis
from atlas.models import SlackToken

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


def get_last_mention(channel, key):
    key = '%s:%s' % (channel, key)
    last = redis.getset(key, time.time())
    if last:
        last = datetime.utcfromtimestamp(float(last))
    return last


@bp.route('/webhooks/jira', methods=['POST'])
@use_args(webhook_args)
def on_msg(args):
    if not SlackToken.is_valid(args['token']):
        log.warning('Invalid token: %s', args['token'])
        abort(401)

    if args['user_name'] == 'slackbot':
        # Avoid infinite feedback loop of bot parsing it's own messages :)
        return Response()

    channel = args['channel_name']

    issue_keys = jira_key_re.findall(args['text'])
    if issue_keys:
        log.info('Message from %s in #%s contained JIRA issue key(s): %s',
                 args['user_name'], channel, ', '.join(issue_keys))

        # Login to JIRA
        authinfo = (
            current_app.config['JIRA_USERNAME'],
            current_app.config['JIRA_PASSWORD'],
        )
        jira_url = current_app.config['JIRA_URL']
        options = {'check_update': False}
        jira = JIRA(jira_url, basic_auth=authinfo, options=options)

        # Retrieve issue(s)
        attachments = []
        for issue_key in issue_keys:
            try:
                last_mention = get_last_mention(channel, issue_key)
                if last_mention:
                    log.debug('%s last mentioned in #%s at %s', issue_key, channel, last_mention)
                    blackout = current_app.config['JIRA_ID_BLACKOUT_PERIOD']
                    if datetime.now() <= last_mention + blackout:
                        continue
                issue = jira.issue(issue_key)
                attachments.append(format_attachment(issue))
            except JIRAError as e:
                if e.status_code == 404:
                    log.warning('%s does not exist', issue_key)
                else:
                    log.error('Error looking up %s: %s', issue_key, e.text)

        if attachments:
            return jsonify({
                'attachments': attachments,
            })

    return Response()


_issue_colors = {
    'Bug': '#D24331',
    'Story': '#65AC43',
    'Task': '#377DC6',
    'Sub-task': '#377DC6',
    'Epic': '#47335D',
}


def format_attachment(issue):
    issue_link = os.path.join(
        current_app.config['JIRA_URL'],
        'browse',
        issue.key
    )

    if issue.fields.assignee:
        assignee = issue.fields.assignee.displayName
    else:
        assignee = '(Unassigned)'

    fields = [
        {
            'title': 'Status',
            'value': issue.fields.status.name,
            'short': True,
        },
        {
            'title': 'Assignee',
            'value': assignee,
            'short': True,
        },
    ]

    title = '%s: %s' % (issue.key, issue.fields.summary)
    attachment = {
        'title': title,
        'title_link': issue_link,
        'fields': fields,
        'fallback': title,
        'color': _issue_colors.get(issue.fields.issuetype.name, None),
    }
    return attachment
