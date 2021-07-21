# encoding:utf-8
from flask import Flask, url_for, redirect, request, flash, jsonify
from flask import render_template

import src.static.py.sql as db_helper
import src.static.py.form as form_template
import folium

import json

from src.static.py import config

app = Flask(__name__, static_folder="./static", template_folder="./templates")
app.config.from_object(config)


@app.route('/')
def hello_world():
    return render_template('login.html')


@app.route('/login', methods=('POST', 'GET'))
def login():
    if request.method == "POST":
        request_json = json.loads(request.get_json())
        work_type = request_json['type']
        name = request_json['type']
        password = request_json['type']

        print(type(name))
        print(name)
        print(type(password))
        print(password)

        if work_type == 'login':

            # 验证

            # sql
            sql = "select Password from users where UserName='{0}' ".format(name)
            result = db_helper.select_one(sql)

            print(result[0])
            print(name)
            print(name == result[0])

            if result[0] == password:
                # 登录成功
                response = {"status": True, "url": url_for('index')}
                return jsonify(response)
            else:
                # 密码错误
                response = {"status": False, "error_text": url_for('index')}
                return jsonify(response)

        elif work_type == 'enroll':

            # 验证

            # enroll
            sql = "insert into webgis_design.users (UserName,Password,Permission) " \
                  "values ('{0}','{1}','{2}')".format(name, password, 0)

            print(sql)
            status = db_helper.update_database(sql)

            if status != 0:
                # 注册成功
                response = {"status": True, "url": url_for('url')}
                return jsonify(response)
            else:
                # 用户名重复，注册失败
                response = {"status": False, "error_text": "用户名重复，请重试 !!"}
                return '注册失败，请重试'
        else:
            # 错误请求
            return 0

    else:
        return render_template('login.html')


@app.route('/map/init_map')
def init_map():
    return render_template("map/init_map.html")


@app.route('/map/heat_map/heat_location')
def heat_location():
    return render_template("map/heat_map/heat_location.html")


@app.route('/map/heat_map/heat_price')
def heat_price():
    return render_template("map/heat_map/heat_price.html")


@app.route('/index')
def index():
    return render_template('index.html', init_map=url_for('init_map'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=100, debug=True)
