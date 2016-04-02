# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located
in __init__.py
"""

from opbeat.contrib.flask import Opbeat
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_sslify import SSLify

opbeat = Opbeat()
redis = FlaskRedis()
db = SQLAlchemy()
migrate = Migrate()
sslify = SSLify()
