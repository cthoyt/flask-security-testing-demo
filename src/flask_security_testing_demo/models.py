# -*- coding: utf-8 -*-

from flask_security import RoleMixin, UserMixin
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship

ROLE_TABLE_NAME = 'role'
USER_TABLE_NAME = 'user'
ROLE_USER_TABLE_NAME = 'roles_users'

Base = declarative_base()

roles_users = Table(
    ROLE_USER_TABLE_NAME,
    Base.metadata,
    Column('user_id', Integer, ForeignKey('{}.id'.format(USER_TABLE_NAME)), primary_key=True),
    Column('role_id', Integer, ForeignKey('{}.id'.format(ROLE_TABLE_NAME)), primary_key=True)
)


class User(Base, UserMixin):
    """User Table"""
    __tablename__ = USER_TABLE_NAME

    id = Column(Integer, primary_key=True)

    email = Column(String(255), unique=True)
    password = Column(String(255))

    active = Column(Boolean)
    confirmed_at = Column(DateTime)

    roles = relationship('Role', secondary=roles_users, backref=backref('users', lazy='dynamic'))


class Role(Base, RoleMixin):
    """Role Table"""
    __tablename__ = ROLE_TABLE_NAME

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    description = Column(Text)
