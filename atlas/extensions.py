# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located
in __init__.py
"""

from opbeat.contrib.flask import Opbeat
from flask_redis import FlaskRedis

opbeat = Opbeat()
redis = FlaskRedis()
