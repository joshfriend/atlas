#!/usr/bin/env python

import os
from flask_script import Manager, Shell, Server
from flask_migrate import MigrateCommand
from sqlalchemy.exc import IntegrityError

from atlas import create_app
from atlas.models import SlackToken

app = create_app()
manager = Manager(app)
manager.add_command('server', Server())
manager.add_command('db', MigrateCommand)

TokenManager = Manager(usage='Manage webhook tokens')
manager.add_command('token', TokenManager)


@TokenManager.option('token', help='The webhook security token')
@TokenManager.option('-c', '--channel', default='*',
                     help='Channel the token applies to')
@TokenManager.option('-d', '--description', required=True,
                     help='Description of what the token is used for')
def add(token, channel, description):
    try:
        SlackToken.create(
            token=token,
            channel=channel,
            description=description
        )
        print('Token added!')
    except IntegrityError:
        print('Token already exists')


@TokenManager.option('token', help='The webhook security token')
def remove(token):
    t = SlackToken.get(token)
    if t:
        t.delete()
        print('Token removed!')
    else:
        print('No such token!')


@TokenManager.command
def list():
    tokens = SlackToken.query \
        .order_by(SlackToken.channel.asc()) \
        .all()
    print('Registered tokens:')
    for token in tokens:
        print(token)


if __name__ == '__main__':
    manager.run()
