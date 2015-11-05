#!/usr/bin/env python

import logging

from flask import Blueprint
from flask.ext.restful import Api, fields

api_v1_blueprint = Blueprint("api_v1", __name__, url_prefix='/api/v1')

log = logging.getLogger('api')

# Import the resources to add the routes to the blueprint before the app is
# initialized
from . import webhook
