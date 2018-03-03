# -*- coding: utf-8 -*-

from flask import Flask
from flask_security import SQLAlchemyUserDatastore, Security
from flask_sqlalchemy import SQLAlchemy

from flask_security_testing_demo.models import Base, Role, User


class FlaskDemo(Flask):
    """A wrapper around a standard :class:`flask.Flask` to make the database, datastore, and security extensions
    easily accessible for testing"""

    def __init__(self, connection: str):
        """
        :param connection: The SQLAlchemy connection string
        """
        super(FlaskDemo, self).__init__(__name__)

        # Add SQLAlchemy settings to application configuration
        self.config['SQLALCHEMY_DATABASE_URI'] = connection
        self.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)

        # Initialize a SQLAlchemy database connection that matches the scope/context of the application
        self.db = SQLAlchemy(app=self)

        Base.metadata.bind = self.db.engine
        Base.query = self.db.session.query_property()

        # Use the SQLAlchemy connection and User/Role class to instantiate a user data store
        self.datastore = SQLAlchemyUserDatastore(
            db=self.db,
            user_model=User,
            role_model=Role
        )

        # Initialize security on this application
        self.security = Security(
            app=self,
            datastore=self.datastore
        )

    def create_all(self):
        """Creates all tables"""
        Base.metadata.create_all()


def create_application(connection: str) -> Flask:
    """Creates an application. Still needs views to be registered later

    :param connection: The SQLAlchemy connection string
    :return: A Flask application
    """
    return FlaskDemo(connection)
