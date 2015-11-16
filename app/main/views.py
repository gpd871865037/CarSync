#coding:utf-8
from flask import Flask, url_for, redirect, flash, jsonify
from flask import request, make_response
from urllib import urlencode
from flask import render_template
from . import main
from models import User, Car, Car_info
from models import db
import datetime, httplib
import requests
import time
import hashlib
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


@main.route('/bind_account')
def bind_account():
    code = request.args.get('code')
    appid = "wx54073d86056904da"
    secret = "e102c09b6828c759084407bebc785b08&code"
    data = requests.get("https://api.weixin.qq.com/sns/oauth2/access_token?" + appid + "&secret=" + secret + "&code="+ code +"&grant_type=authorization_code")
    result = json.loads(data.text)
    openid = result.get('openid')
    return render_template('bind_account.html', code=openid)


@main.route('/get_info', methods=['POST'])
def get_info():
    openid = request.form["code"]
    phone = request.form["phone"]
    user = User.query.filter_by(weixin_id=openid).first()

    if user is None:
        # times = datetime.datetime(time.localtime(time.time()))
        # created = time.strptime(times, '%Y-%m-%d %H:%M:%S')
        times = datetime.datetime.now()

        user = User(weixin_id=openid, phone=phone, created_times=times)
        db.session.add(user)
        db.session.commit()

        if user != None:
            # return redirect()
            return 'success'
        else:
            flash("绑定失败，请在公众号重新绑定")
            return render_template('bind_account.html', code=openid)
    else:
        flash("账号已绑定，跳转到个人页面")
        return render_template('bind_account.html', code=openid)


@main.route('/new_vehicle')
def new_vehicle():
    return render_template('new_vehicle.html')


@main.route('/index_vehicle')
def index_vehicle():
    return render_template('index_vehicle.html')


# TODO 动态创建菜单的方法
@main.route('/check_signature')
def check_signature():
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')

    token = "QWIEKS9HAS128SDH3897SD10SD8132EJ"
    signature_list = sorted([token, timestamp, nonce])
    signature_str = ''.join(signature_list)

    if hashlib.sha1(signature_str).hexdigest() == signature:
        return make_response(echostr)
    else:
        return None
    # TODO 同上
    #return redirect('/bind_account')


# FIXME 暂时先注释掉验证服务器的方法，转而接受微信的POST请求
@main.route('/get_access_token')
def get_access_token():
    app_id = "wx54073d86056904da"
    app_secret = "e102c09b6828c759084407bebc785b08"
    r = requests.get("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + app_id + "&secret=" + app_secret)
    if r.status_code == 200:
        return make_response(r.text)
    else:
        return None


@main.route('/post_car')
def post_car():
    code = request.args.get('code')
    appid = "wx54073d86056904da"
    secret = "e102c09b6828c759084407bebc785b08&code"
    data = requests.get("https://api.weixin.qq.com/sns/oauth2/access_token?" + appid + "&secret=" + secret + "&code="+ code +"&grant_type=authorization_code")
    result = json.loads(data.text)
    openid = result.get('openid')

    user = User.query.filter_by(weixin_id=openid).first()
    if user is None:
        flash("账号未绑定")
        return render_template('post_car.html')
    cars = Car.query.group_by("brand").all()
    return render_template('post_car.html', cars=cars, code=openid)


@main.route('/insert_car')
def insert_car():
    f = open('cars.json','r')
    carlist = f.read()
    f.close()
    cars = json.loads(carlist)
    i = 0
    for x in cars:
        print x['id'],x["Brand_id"],x["Brand"],x["Car_id"],x["Car"],x["Model_id"],x["Model"]
        car = Car(brand_id=x["Brand_id"], brand=x["Brand"], car_id=x["Car_id"], car=x["Car"], model_id=x["Model_id"], model=x["Model"])
        db.session.add(car)
        db.session.commit()
        if i > 1000:
            break
        i += 1
    return "1"


@main.route('/get_car', methods=['POST'])
def get_car():
    brand = request.form["brand"]
    data = Car.query.filter_by(brand_id=brand).group_by("car").all()
    return jsonify(json_list=[i.serialize for i in data])


@main.route('/get_model', methods=['POST'])
def get_model():
    model = request.form["model"]
    data = Car.query.filter_by(model_id=model).group_by("model").all()
    print "======================================"
    print model
    print data
    return jsonify(json_list=[i.serialize for i in data])


@main.route('/post_car_information', methods=['POST'])
def post_car_information():
    openid = request.form["code"]
    brand_id = request.form["brand"]
    car_id = request.form["car"]
    model_id = request.form["model"]
    color = request.form["color"]
    first_license_time = request.form["first_license_time"]
    maintenance = request.form["maintenance"]
    accident = request.form["accident"]
    inspection = request.form["inspection"]
    compulsory_insurance = request.form["compulsory_insurance"]
    commercial_insurance = request.form["commercial_insurance"]
    mileage = request.form["mileage"]
    price = request.form["price"]
    title = request.form["title"]
    description = request.form["description"]
    information = request.form["information"]
    contacts = request.form["contacts"]
    contact_number = request.form["contact_number"]

    car_info = Car_info(weixin_id=openid,brand_id=brand_id, car_id=car_id, model_id=model_id, color=color, first_license_time=first_license_time, maintenance=maintenance,
                        accident=accident, inspection=inspection, compulsory_insurance=compulsory_insurance, commercial_insurance=commercial_insurance, mileage=mileage,
                        price=price, title=title,description=description, information=information, contacts=contacts, contact_number=contact_number)
    db.session.add(car_info)
    db.session.commit()

    if car_info.id is not None:
        return 'success'
    else:
        flash("发布失败，请重新发布")
        cars = Car.query.group_by("brand").all()
        return render_template('post_car.html', code=openid, cars=cars)