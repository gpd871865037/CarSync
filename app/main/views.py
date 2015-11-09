#coding:utf-8
from flask import Flask, url_for, redirect,flash
from flask import request, make_response
from urllib import urlencode
from flask import render_template
from . import main
from models import User, Car
from models import db
import datetime
import requests
import time
import hashlib
import json


@main.route('/bind_account')
def bind_account():
    code = request.args.get('code')
    appid = "wx54073d86056904da"
    secret = "e102c09b6828c759084407bebc785b08&code"
    data = requests.get("https://api.weixin.qq.com/sns/oauth2/access_token?" + appid + "&secret=" + secret + "&code="+ code +"&grant_type=authorization_code")
    result = json.loads(data.text)
    openid = result.get('openid')
    return render_template('bind_account.html',code=openid)


@main.route('/get_info', methods=['POST'])
def get_info():
    openid = request.form["code"]
    phone = request.form["phone"]
    user = User.query.filter_by(weixin_id=openid).first()

    if user.equals(None):
        # times = datetime.datetime(time.localtime(time.time()))
        # created = time.strptime(times, '%Y-%m-%d %H:%M:%S')
        times = datetime.datetime.now()

        user = User(weixin_id=openid, phone=phone, created_times=times)
        db.session.add(user)
        db.session.commit()

        if user.equals(None):
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
    car = Car.query.first();
    return render_template('post_car.html', car=car)


@main.route('/insert_car')
def insert_car():
    f = open('cars.json','r')
    carlist = f.read()
    f.close()
    cars = json.loads(carlist)
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
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
