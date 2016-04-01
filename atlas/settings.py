#!/usr/bin/env python

import os
import logging
from datetime import timedelta


class Config(object):
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    LOG_FORMAT = '%(name)-12s | %(levelname)-8s | %(message)s'
    DEFAULT_LOG_LEVEL = logging.DEBUG
    LOG_LEVEL = os.getenv('LOG_LEVEL')

    SLACK_TEAM_DOMAIN = os.getenv('SLACK_TEAM_DOMAIN')
    SLACK_WEBHOOK_TOKENS = os.getenv('SLACK_WEBHOOK_TOKENS', '').split(',')

    JIRA_URL = os.getenv('JIRA_URL')
    JIRA_USERNAME = os.getenv('JIRA_USERNAME')
    JIRA_PASSWORD = os.getenv('JIRA_PASSWORD')
    JIRA_ID_BLACKOUT_PERIOD = timedelta(seconds=int(os.getenv('JIRA_ID_BLACKOUT_PERIOD', 300)))

    OPBEAT = {
        'ORGANIZATION_ID': os.getenv('OPBEAT_ORG_ID'),
        'APP_ID': os.getenv('OPBEAT_APP_ID'),
        'SECRET_TOKEN': os.getenv('OPBEAT_SECRET_TOKEN'),
        'INCLUDE_PATHS': ['demo']
    }

    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/1')

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
