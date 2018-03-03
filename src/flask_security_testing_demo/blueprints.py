# -*- coding: utf-8 -*-

from flask import Blueprint
from flask_security import roles_accepted, roles_required

api_blueprint = Blueprint(__name__, 'api')


@api_blueprint.route('/')
def view_public():
    return 'public'


@api_blueprint.route('/required')
@roles_required('admin')
def view_required():
    return 'required'


@api_blueprint.route('/accepted')
@roles_accepted('admin', 'beta')
def view_accepted():
    return 'accepted'
