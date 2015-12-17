#coding:utf-8
from flask import Flask, url_for, redirect, flash, jsonify
from flask import request, make_response
from urllib import urlencode
from flask import render_template
from . import main
from models import User, Car, Car_info, Car_image
from models import db
from datetime import datetime, date, time
from werkzeug import secure_filename
from app.lib.upload_file import uploadfile
import string
import uuid
import requests
import simplejson
import hashlib
import json
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')


# UPLOAD_FOLDER = '/Code/Python/CarSync/app/static/img'
UPLOAD_FOLDER = '/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
APPID = "wx54073d86056904da"
SECRET = "e102c09b6828c759084407bebc785b08"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['APPID'] = APPID
app.config['SECRET'] = SECRET


def get_openid(code):
    appid = app.config['APPID']
    secret = app.config['SECRET']
    data = requests.get("https://api.weixin.qq.com/sns/oauth2/access_token?appid=" + appid + "&secret=" + secret + "&code="+ code +"&grant_type=authorization_code")
    result = json.loads(data.text)
    openid = result.get('openid')
    return openid


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def gen_file_name(filepath, filename):
    filepath = filepath + '/' + filename[0:6]
    # while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
    # filename = '%s_%s%s' % (name, str(i), extension)
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    return filepath

def get_img_id(img_list):
    img_id = []
    for img in img_list:
        path = img
        image = Car_image(path=path)
        db.session.add(image)
        db.session.commit()
        img_id.append(str(image.id))
    ids = string.join(img_id, ",")
    return ids

def get_uploads_path(path):
    base = path[-6:]
    return base

@main.route('/bind_account')
def bind_account():
    code = request.args.get('code')
    openid = get_openid(code)
    print openid,"-----------------------------------------"
    return render_template('bind_account.html', code=openid)


@main.route('/get_info', methods=['POST'])
def get_info():
    openid = request.form["code"]
    phone = request.form["phone"]
    user = User.query.filter_by(weixin_id=openid).first()

    if user is None:
        # times = datetime.datetime(time.localtime(time.time()))
        # created = time.strptime(times, '%Y-%m-%d %H:%M:%S')
        times = datetime.now()

        user = User(weixin_id=openid, phone=phone, created_times=times)
        db.session.add(user)
        db.session.commit()

        if user.id is not None:
            # return redirect()
            return '账号成功绑定'
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
# @main.route('/get_access_token')
# def get_access_token():
#     app_id = "wx54073d86056904da"
#     app_secret = "e102c09b6828c759084407bebc785b08"
#     r = requests.get("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + app_id + "&secret=" + app_secret)
#     if r.status_code == 200:
#         return make_response(r.text)
#     else:
#         return None


@main.route('/post_car')
def post_car():
    code = request.args.get('code')
    openid = get_openid(code)
    # openid = '1234324234'

    exitis = False
    user = User.query.filter_by(weixin_id=openid).first()
    if user is None:
        exitis = True
    cars = Car.query.group_by("brand").all()
    return render_template('post_car.html', cars=cars, exitis=exitis, code=openid)


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
    data = Car.query.filter_by(car_id=model).group_by("model").all()
    return jsonify(json_list=[i.serialize for i in data])


@main.route('/post_car_information', methods=['POST'])
def post_car_information():
    if request.files['file'] is not None :
        file = request.files['file']
        #pprint (vars(objectvalue))
        if file:
            filename = secure_filename(file.filename)
            # filename = gen_file_name(filename)
            filename = str(uuid.uuid1()) + '.' + filename.rsplit('.', 1)[1].lower()
            print filename,"++++++++++++++++++++++++++++++++++++++++++++"
            mimetype = file.content_type
            # set upload url
            filepath = gen_file_name(app.config['UPLOAD_FOLDER'], filename)
            print filepath,"++++++++++++++++++++++++++++++++++++++++++++"


            if not allowed_file(file.filename):
                result = uploadfile(name=filename, type=mimetype, size=0, not_allowed_msg="Filetype not allowed")

            else:
                # save file to disk
                uploaded_file_path = os.path.join(filepath, filename)
                file.save(uploaded_file_path)

                # get file size after saving
                size = os.path.getsize(uploaded_file_path)

                # return json for js call back
                result = uploadfile(name=filename, type=mimetype, size=size, path=get_uploads_path(filepath))

            return simplejson.dumps({"files": [result.get_file()]})


    image_id = get_img_id(request.form.getlist("imgUrl[]"))
    # openid = '1234456'
    openid = request.form["code"]
    brand_id = request.form["brand"]
    car_id = request.form["car"]
    model_id = request.form["model"]
    color = request.form["color"]
    first_license_time = datetime.strptime(request.form["first_license_time"], "%Y-%m-%d")
    maintenance = request.form["maintenance"]
    accident = request.form["accident"]
    inspection = datetime.strptime(request.form["inspection"], "%Y-%m-%d")
    compulsory_insurance = datetime.strptime(request.form["compulsory_insurance"], "%Y-%m-%d")
    commercial_insurance = datetime.strptime(request.form["commercial_insurance"], "%Y-%m-%d")
    mileage = request.form["mileage"]
    price = request.form["price"]
    title = request.form["title"]
    description = request.form["description"]
    information = request.form["information"]
    contacts = request.form["contacts"]
    contact_number = request.form["contact_number"]

    car_info = Car_info(weixin_id=openid, brand_id=brand_id, car_id=car_id, model_id=model_id, color=color, first_license_time=first_license_time, maintenance=maintenance,
                        accident=accident, mileage=mileage, inspection=inspection, compulsory_insurance=compulsory_insurance, commercial_insurance=commercial_insurance,
                        price=price, title=title,description=description, information=information, contacts=contacts, contact_number=contact_number, image_id=image_id)
    db.session.add(car_info)
    db.session.commit()

    if car_info.id is not None:
        return 'success'
    else:
        flash("发布失败，请重新发布")
        cars = Car.query.group_by("brand").all()
        return render_template('post_car.html', code=openid, cars=cars)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@main.route('/post_car_image')
def post_car_image():
    if request.files['file'] is not None:
        return simplejson.dumps({"files": [{'size': 111, 'name': 'city.jpg', 'url' : 'localhost:5000/static/images/city.jpg' }]})
    # if request.method == 'POST':
    #     file = request.files['file']
    #     if file and allowed_file(file.filename):
    #         filename = file.filename
    #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #         return redirect(url_for('uploaded_file',
    #                                 filename=filename))


@main.route('/car_list')
def car_list():
    code = request.args.get('code')
    openid = get_openid(code)
    data = User.query.filter_by(weixin_id=openid).all()
    if data is None:
        return redirect("/bind_account?openid=" + openid)
    car_info = Car_info.query.filter_by(weixin_id=openid).all()
    for info in car_info:
        id = info.image_id.split(",")[0]
        car_first_image = Car_image.query.filter_by(id=id).first()
        url = car_first_image.path
        car = Car.query.filter_by(brand_id=info.brand_id).first()
        info.brand = car.brand
        car = Car.query.filter_by(car_id=info.car_id).first()
        info.car = car.car
        car = Car.query.filter_by(model_id=info.model_id).first()
        info.model = car.model
        info.url = url
    return render_template('car_info_list.html', car_info=car_info)


