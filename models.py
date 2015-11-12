from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
import os


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    weixin_id = db.Column(db.Integer, unique=True, index=True)
    phone = db.Column(db.Integer)
    created_times = db.Column(db.DATETIME)
    updated_times = db.Column(db.DATETIME)
    deleted_times = db.Column(db.DATETIME)

    def repr(self):
        return '<User %r>' % self.username

class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    brand_id = db.Column(db.Integer)
    brand = db.Column(db.String)
    car_id = db.Column(db.Integer)
    car =  db.Column(db.String)
    model_id = db.Column(db.Integer)
    model  =  db.Column(db.String)

    def repr(self):
        return '<User %r>' % self.username

    @property
    def serialize(self):
       return {
           'id'      : self.id,
           'brand_id': self.brand_id,
           'brand'   : self.brand,
           'car_id'  : self.car_id,
           'car'     : self.car,
           'model_id': self.model_id,
           'model'   : self.model
       }