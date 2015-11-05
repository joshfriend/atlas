#!/usr/bin/env python

'''The atlas module, containing the app factory function.'''

import os
import logging

from flask import Flask

from atlas.settings import ProdConfig, DevConfig
from atlas.extensions import (
    opbeat,
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
    opbeat.init_app(app)
    register_extensions(app)
    register_blueprints(app)
    configure_logging(app)
    return app


def register_extensions(app):
    pass


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
    level = log_levels.get(os.getenv('LOG_LEVEL'), default_level)
    logging.basicConfig(format=app.config['LOG_FORMAT'],
                        datefmt=app.config['LOG_DATE_FORMAT'])

    log.setLevel(level)
