__author__ = 'candys'

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "82USYXHWKSIW28SY"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True