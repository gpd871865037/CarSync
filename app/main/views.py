#coding:utf-8
from flask import request, make_response
from flask import render_template
from . import main
import requests
import hashlib
import json


@main.route('/bind_account')
def bind_account():
    return render_template('bind_account.html')


@main.route('/new_vehicle')
def new_vehicle():
    return render_template('new_vehicle.html')


@main.route('/index_vehicle')
def index_vehicle():
    return render_template('index_vehicle.html')


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



@main.route('/get_access_token')
def get_access_token():
    app_id = "wx606d7782e48067f8"
    app_secret = "edaaca8066c752ccd826a41cd43c9bd6"
    r = requests.get("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + app_id + "&secret=" + app_secret)
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        return False
