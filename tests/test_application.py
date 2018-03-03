# -*- coding: utf-8 -*-

"""Test the Flask application as well as possible using the documentation from
http://flask.pocoo.org/docs/0.12/testing/"""

import os
import tempfile
import unittest
from contextlib import contextmanager
from unittest.mock import Mock, patch

from flask_security import current_user

from flask_security_testing_demo import FlaskDemo, Role, User, api_blueprint


# TODO: add testing for what the current user is. Currently, anonymous users are None, instead of being instantiated

class TestApplication(unittest.TestCase):

    @contextmanager
    def login(self, user):
        mock_get_user = patch('flask_login.utils._get_user', Mock(return_value=user))
        mock_get_user.start()
        yield
        mock_get_user.stop()

    def setUp(self):
        self.fd, self.path = tempfile.mkstemp()
        self.connection = 'sqlite:///' + self.path

        # Use subclass of flask.Flask to make some of this code a bit prettier
        self.app = FlaskDemo(self.connection)
        self.app.secret_key = 'testing, so why bother with a secret key?'
        self.app.register_blueprint(api_blueprint)

        # Create tables with example roles and users
        self.app.create_all()

        self.app.datastore.create_role(name='admin')
        self.app.datastore.create_role(name='beta')

        self.user_admin = self.app.datastore.create_user(email='admin@example.com', roles=['admin', 'beta'])
        self.user_beta = self.app.datastore.create_user(email='beta@example.com', roles=['beta'])
        self.user_example = self.app.datastore.create_user(email='public@example.com')

        self.app.datastore.commit()

        # Create a test client
        self.client = self.app.test_client()

        # push the context
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        os.close(self.fd)
        os.remove(self.path)

    def test_models(self):
        """Checks all models were added properly"""

        r = self.app.datastore.find_role('admin')
        self.assertIsNotNone(r)
        self.assertIsInstance(r, Role)
        self.assertEqual('admin', r.name)

        u = self.app.datastore.find_user(email='admin@example.com')
        self.assertIsNotNone(u)
        self.assertIsInstance(u, User)
        self.assertEqual('admin@example.com', u.email)
        self.assertTrue(u.has_role('admin'))

    def test_anonymous_public(self):
        """Tests that an anonymous user can access the public endpoint"""
        rv = self.client.get('/')
        self.assertEqual(b'public', rv.data)

    def test_anonymous_required_failure(self):
        """Tests that a failure happens when an anonymous user tries to access the roles required endpoint"""
        rv = self.client.get('/required', follow_redirects=True)
        self.assertNotEqual(b'required', rv.data)

    def test_anonymous_accepted_failure(self):
        """Tests that a failure happens when an anonymous user tries to access the roles accepted endpoint"""
        rv = self.client.get('/accepted')
        self.assertNotEqual(b'accepted', rv.data)

    def test_admin_public(self):
        """Tests that an admin user still gets access to the public endpoint"""
        with self.login(self.user_admin):
            self.assertTrue(current_user.is_authenticated)
            self.assertEqual(current_user, self.user_admin)

            rv = self.client.get('/')
            self.assertEqual(b'public', rv.data)

    def test_admin_required(self):
        """Tests that an admin user can access the required endpoint"""
        with self.login(self.user_admin):
            self.assertTrue(current_user.is_authenticated)
            self.assertEqual(current_user, self.user_admin)

            rv = self.client.get('/required')
            self.assertEqual(b'required', rv.data)
