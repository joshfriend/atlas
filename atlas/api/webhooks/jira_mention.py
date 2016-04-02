#!/usr/bin/env python

import re
import os
import time
from datetime import datetime

from flask import Response, current_app, jsonify
from webargs.flaskparser import use_args
from jira import JIRA, JIRAError

from atlas.api import api_v1_blueprint as bp, ignore_slackbot
from atlas.api.webhooks import log, webhook_args
from atlas.extensions import redis

jira_key_re = re.compile(r'[A-Z]+-\d+')


def get_last_mention(channel, key):
    key = '%s:%s' % (channel, key)
    last = redis.getset(key, time.time())
    if last:
        last = datetime.utcfromtimestamp(float(last))
    return last


@bp.route('/webhooks/jira', methods=['POST'])
@use_args(webhook_args)
@ignore_slackbot
def jira_webhook(args):
    return jira_command(args)


def jira_command(args):
    channel = args['channel_name']

    issue_keys = jira_key_re.findall(args['text'])
    if not issue_keys:
        return Response()

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
                log.debug('%s last mentioned in #%s at %s',
                          issue_key, channel, last_mention)
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

    if not attachments:
        return Response()

    return jsonify({
        'response_type': 'in_channel',
        'attachments': attachments,
    })


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
