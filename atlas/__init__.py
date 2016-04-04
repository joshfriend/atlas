#!/usr/bin/env python

'''The atlas module, containing the app factory function.'''

import os
import logging

from flask import Flask

from atlas.settings import ProdConfig, DevConfig
from atlas.extensions import (
    opbeat,
    redis,
    db,
    migrate,
    sslify,
)
from atlas.api import api_v1_blueprint, log

if os.getenv("FLASK_ENV") == 'prod':
    DefaultConfig = ProdConfig
else:
    DefaultConfig = DevConfig


def create_app(config_object=DefaultConfig):
    '''An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    '''
    app = Flask(__name__)
    app.config.from_object(config_object)
    if not app.debug:
        opbeat.init_app(app)
    register_extensions(app)
    register_blueprints(app)
    configure_logging(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    redis.init_app(app)
    sslify.init_app(app, permanent=True)


def register_blueprints(app):
    app.register_blueprint(api_v1_blueprint)


def configure_logging(app):
    log_levels = {
        'error': logging.ERROR,
        'warning': logging.WARNING,
        'info': logging.INFO,
        'debug': logging.DEBUG,
    }
    default_level = app.config['DEFAULT_LOG_LEVEL']
    level = log_levels.get(app.config['LOG_LEVEL'], default_level)
    logging.basicConfig(format=app.config['LOG_FORMAT'])

    log.setLevel(level)

    # Api does its own request logging
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
