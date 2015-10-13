from flask import request
from flask import render_template
from . import main
import requests
import hashlib
import json

# 绑定帐号
@main.route('/bind_account')
def bind_account():
    return render_template('bind_account.html')


# 发布新车源
@main.route('/new_vehicle')
def new_vehicle():
    return render_template('new_vehicle.html')


# 车源发布情况
@main.route('/index_vehicle')
def index_vehicle():
    return render_template('index_vehicle.html')


# 验证微信签名
@main.route('/check_signature')
def check_signature():
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')

    token = "QWIEKS9HAS128SDH3897SD10SD8132EJ"
    signature_list = sorted([token, timestamp, nonce])
    signature_str = ''.join(signature_list)

    if hashlib.sha1(signature_str).hexdigest() == signature:
        return True
    else:
        return False


# 获得微信token
@main.route('/get_access_token')
def get_access_token():
    app_id = "wx54073d86056904da"
    app_secret = "e102c09b6828c759084407bebc785b08"
    r = requests.get("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + app_id + "&secret=" + app_secret)
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        return False
