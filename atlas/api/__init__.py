#!/usr/bin/env python

import logging

from flask import Blueprint, current_app, request

api_v1_blueprint = Blueprint("api_v1", __name__, url_prefix='/api/v1')

log = logging.getLogger('api')


@api_v1_blueprint.after_request
def log_response(response):
    """Log any requests/responses with an error code"""
    if log.getEffectiveLevel() == logging.DEBUG:  # pragma: no cover, debugging only
        log.debug('%7s: %s - %i', request.method, request.url,
                  response.status_code)
        if response.status_code >= 400:
            log.debug('Response data: \n%s', response.data)
            log.debug('Request data: \n%s', request.data)

    return response


# Import the resources to add the routes to the blueprint before the app is
# initialized
from . import webhook
