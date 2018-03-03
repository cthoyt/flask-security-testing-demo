# -*- coding: utf-8 -*-

import os

from flask_security_testing_demo.application import create_application
from flask_security_testing_demo.blueprints import api_blueprint

if __name__ == '__main__':
    connection = 'sqlite:///' + os.path.expanduser('~/Desktop/flask_security_testing_demo.db')
    app = create_application(connection=connection)
    app.register_blueprint(api_blueprint)
    app.secret_key = 'testing'
    app.run()
