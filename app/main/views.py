#coding:utf-8
from flask import Flask, url_for, redirect,flash
from flask import request, make_response
from urllib import urlencode
from flask import render_template
from . import main
from models import User
from models import db
import requests
import time
import hashlib
import json


@main.route('/bind_account')
def bind_account():
    code = request.args.get('code')
    data = requests.get("https://api.weixin.qq.com/sns/oauth2/access_token?appid=wx54073d86056904da&secret=e102c09b6828c759084407bebc785b08&code="+ code +"&grant_type=authorization_code")
    result = json.loads(data.text)
    openid = result['openid'].encode('utf-8')
    print type(result['openid'])
    print type(openid)
    return render_template('bind_account.html', openid=openid)

@main.route('/get_info', methods=['POST'])
def get_info():
    openid = request.form("code")
    phone = request.form("phone")
    user = User.query.filter_by(weixin_id=openid).first()
    # if user == None:
    #     times = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    #     return times
    return 'asdasaf'
        # user = User(weixin_id = openid,phone = phone,created = times)
        # db.session.add(user)
        # db.session.commit()
        # # if user.id != None:
        # # #    return redirect()
        # # else:
        # #     flash("error")


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


