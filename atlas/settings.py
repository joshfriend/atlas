#!/usr/bin/env python

import os
import logging


class Config(object):
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    LOG_FORMAT = '%(asctime)s | %(name)-12s | %(levelname)-8s | %(message)s'
    LOG_DATE_FORMAT = '%m/%d/%Y %H:%M:%S'
    DEFAULT_LOG_LEVEL = logging.DEBUG

    SLACK_TEAM_DOMAIN = os.getenv('SLACK_TEAM_DOMAIN')
    SLACK_WEBHOOK_TOKENS = os.getenv('SLACK_WEBHOOK_TOKENS', '').split(',')

    JIRA_URL = os.getenv('JIRA_URL')
    JIRA_USERNAME = os.getenv('JIRA_USERNAME')
    JIRA_PASSWORD = os.getenv('JIRA_PASSWORD')

    OPBEAT = {
        'ORGANIZATION_ID': os.getenv('OPBEAT_ORG_ID'),
        'APP_ID': os.getenv('OPBEAT_APP_ID'),
        'SECRET_TOKEN': os.getenv('OPBEAT_SECRET_TOKEN'),
        'INCLUDE_PATHS': ['demo']
    }


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
