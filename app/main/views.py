__author__ = 'candys'

from flask import request
from . import main
import requests
import hashlib
import json

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

@main.route('/get_access_token')
def get_access_token():
    app_id = "wx54073d86056904da"
    app_secret = "e102c09b6828c759084407bebc785b08"
    r = requests.get("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + app_id + "&secret=" + app_secret)
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        return False