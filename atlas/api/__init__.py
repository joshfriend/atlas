#!/usr/bin/env python

import logging
import functools

from flask import Blueprint, request, abort, Response, g

from atlas.models import SlackToken

api_v1_blueprint = Blueprint("api_v1", __name__, url_prefix='/api/v1')

log = logging.getLogger('api')


def _get_arg(field):
    if request.method == 'POST':
        return request.form.get(field, None)
    else:
        # GET
        return request.args.get(field, None)


@api_v1_blueprint.before_request
def check_token():
    g.valid_token = False
    token = _get_arg('token')
    if not token:
        log.warning('No token provided!')
    elif SlackToken.is_valid(token):
        log.debug('Valid request token: %s', token)
        g.valid_token = True
    else:
        log.warning('Unkonwn Slack token: %s', token)


@api_v1_blueprint.after_request
def log_response(response):  # pragma: no cover, debugging only
    """Log any requests/responses with an error code"""
    if log.getEffectiveLevel() == logging.DEBUG:
        log.debug('%7s: %s - %i', request.method, request.url,
                  response.status_code)
        if response.status_code >= 400:
            log.debug('Response data:\n%s', response.data)
            log.debug('Request headers:\n%s', request.headers)
            log.debug('Request formdata:\n%s', request.form)

    return response


def ignore_slackbot(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if _get_arg('user_name') == 'slackbot':
            log.debug('Ignored request from slackbot')
            return Response()
        return func(*args, **kwargs)
    return wrapper


def require_token(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not g.valid_token:
            abort(401)
        return func(*args, **kwargs)
    return wrapper


# Import the resources to add the routes to the blueprint before the app is
# initialized
from .webhooks import jira_mention, slash  # noqa
