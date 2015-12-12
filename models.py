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


class Car_info(db.Model):
    __tablename__ = 'car_info'
    id = db.Column(db.Integer, primary_key=True)
    weixin_id = db.Column(db.Integer, index=True)
    brand_id = db.Column(db.Integer)
    car_id = db.Column(db.Integer)
    model_id = db.Column(db.Integer)
    color = db.Column(db.String)
    first_license_time = db.Column(db.DATETIME)
    maintenance = db.Column(db.Integer)
    accident = db.Column(db.Integer)
    inspection = db.Column(db.DATETIME)
    compulsory_insurance = db.Column(db.DATETIME)
    commercial_insurance = db.Column(db.DATETIME)
    mileage = db.Column(db.Integer)
    price = db.Column(db.Integer)
    title = db.Column(db.String)
    description = db.Column(db.String)
    information = db.Column(db.String)
    contacts = db.Column(db.String)
    contact_number = db.Column(db.String)
    image_id = db.Column(db.String)

    def repr(self):
        return '<User %r>' % self.username

class Car_image(db.Model):
    __tablename__ = 'car_image'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String)

    def repr(self):
        return '<User %r>' % self.username
