#!/usr/bin/env python

import os
import logging
from datetime import timedelta


def env_int(name, default=0):
    return int(os.getenv(name, default))


def env_list(name, sep=','):
    return os.getenv(name, '').split(sep)


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'asdf')

    LOG_FORMAT = '%(name)-12s | %(levelname)-8s | %(message)s'
    DEFAULT_LOG_LEVEL = logging.DEBUG
    LOG_LEVEL = os.getenv('LOG_LEVEL')

    JIRA_URL = os.getenv('JIRA_URL')
    JIRA_USERNAME = os.getenv('JIRA_USERNAME')
    JIRA_PASSWORD = os.getenv('JIRA_PASSWORD')
    JIRA_ID_BLACKOUT_PERIOD = timedelta(
        seconds=env_int('JIRA_ID_BLACKOUT_PERIOD', 300)
    )

    OPBEAT = {
        'ORGANIZATION_ID': os.getenv('OPBEAT_ORG_ID'),
        'APP_ID': os.getenv('OPBEAT_APP_ID'),
        'SECRET_TOKEN': os.getenv('OPBEAT_SECRET_TOKEN'),
        'INCLUDE_PATHS': ['demo']
    }

    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/1')

    _DEFAULT_DB = 'postgresql://atlas:atlas@localhost:5432/atlas'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', _DEFAULT_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
    ADMIN_USERNAME = os.getenv('ADMIN_PASSWORD')


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False


class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True


class TestConfig(Config):
    """Test configuration."""
    ENV = 'test'
    TESTING = True
    DEBUG = True
