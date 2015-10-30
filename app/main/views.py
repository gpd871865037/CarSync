#coding:utf-8
from flask import Flask, url_for, redirect,flash
from flask import request, make_response
from urllib import urlencode
from flask import render_template
from . import main
from models import User
from models import db
import datetime
import requests
import time
import hashlib
import json


# TODO 方法与方法之间空两行
# TODO appid和secret两个参数使用变量来保存，再放到url里，这里的原则是：凡是以后可能会变的参数，一律摘出来。以后当这类变量变多，或项目变复杂后，可以单独写一个文件来全局存储配置信息。
@main.route('/bind_account')
def bind_account():
    code = request.args.get('code')
    data = requests.get("https://api.weixin.qq.com/sns/oauth2/access_token?appid=wx54073d86056904da&secret=e102c09b6828c759084407bebc785b08&code="+ code +"&grant_type=authorization_code")
    result = json.loads(data.text)
    openid = result.get('openid')
    return render_template('bind_account.html',code=openid)


@main.route('/get_info', methods=['POST'])
def get_info():
    openid = request.form["code"]
    phone = request.form["phone"]
    user = User.query.filter_by(weixin_id=openid).first()
    # TODO 除了字符串、整型等简单类型可以用＝＝来判断外，复杂类型如对象类型None类型一律使用equals判断。如user.equals(None)
    if user.equals(None):
        # TODO 注释必须以 #+空格 开头
        #times = datetime.datetime(time.localtime(time.time()))
        #created = time.strptime(times, '%Y-%m-%d %H:%M:%S')
        times = datetime.datetime.now()
        # TODO 方法里给指定参数传值，＝的左右不需要空格，如code=openid
        # TODO 方法里给参数传值，参数与参数之间的,逗号之后加一个空格，如User(weixin_id=openid, phone=phone)
        user = User(weixin_id = openid,phone = phone,created_times=times)
        db.session.add(user)
        db.session.commit()
        # TODO 修改意见同上
        if user.id != None:
            # TODO 无效的行删掉，同上，注释以 #+空格 开头，紧贴语句
        #    return redirect()
            return 'success'
        else:
            flash("绑定失败，请在公众号重新绑定")
            # TODO 方法里给指定参数传值，＝的左右不需要空格，如code=openid
            return render_template('bind_account.html',code = openid)
    else:
        flash("账号已绑定，跳转到个人页面")
        # TODO 同上
        return render_template('bind_account.html',code = openid)


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
    # TODO 这里明显appid和secret两次使用了，应考虑找一个地方专门存配置
    app_id = "wx54073d86056904da"
    app_secret = "e102c09b6828c759084407bebc785b08"
    r = requests.get("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + app_id + "&secret=" + app_secret)
    if r.status_code == 200:
        return make_response(r.text)
    else:
        return None


