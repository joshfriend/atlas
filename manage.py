#!/usr/bin/env python

import os
from flask.ext.script import Manager, Shell, Server
from flask_migrate import MigrateCommand

from atlas import create_app

app = create_app()

manager = Manager(app)

manager.add_command('server', Server())
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
