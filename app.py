# encoding:utf-8
from flask import Flask, url_for, redirect, request, jsonify
from flask import render_template

import src.static.py.sql as db_helper
import src.static.py.validate as validate_helper
from src.static.py import config

app = Flask(__name__, static_folder="./static", template_folder="./templates")
app.config.from_object(config)


@app.route('/')
def hello():
    url = url_for('login')
    return redirect(url)


@app.route('/login', methods=('POST', 'GET'))
def login():
    if request.method == "POST":
        request_json = request.get_json(force=True)
        work_type = request_json['type']
        name = request_json['name']
        password = request_json['password']

        # print(work_type)
        # print(type(name))
        # print(name)
        # print(type(password))
        # print(password)

        if work_type == 'login':

            # 验证
            status = validate_helper.validate(name, password)

            if status == "success validate":
                # sql
                sql = "select Password from users where UserName='{0}' ".format(name)
                result = db_helper.select_one(sql)

                print(sql)
                # print(result[0])
                # print(name)
                # print(password == result[0])

                if result[0] == password:
                    # 登录成功
                    response = {"status": True, "url": url_for('index')}
                    return jsonify(response)
                else:
                    # 密码错误
                    response = {"status": False, "error_text": "密码错误，请重试！！"}
                    return jsonify(response)
            else:
                response = {"status": False, "error_text": status}
                return jsonify(response)

        elif work_type == 'enroll':

            # 验证
            status = validate_helper.validate(name, password)

            if status == "success validate":
                # enroll
                sql = "insert into webgis_design.users (UserName,Password,Permission) " \
                      "values ('{0}','{1}','{2}')".format(name, password, 0)

                print(sql)
                status = db_helper.update_database(sql)

                if status != 0:
                    # 注册成功
                    response = {"status": True, "url": url_for('login')}
                    return jsonify(response)
                else:
                    # 用户名重复，注册失败
                    response = {"status": False, "error_text": "用户名重复，请重试 !!"}
                    return jsonify(response)
            else:
                response = {"status": False, "error_text": status}
                return jsonify(response)
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
    if request.method == "POST":
        request_json = request.get_json(force=True)
        work_type = request_json['type']

        print(work_type)

        # 房价点绘制显示
        if work_type == 'house':
            return 0

        # 医院点绘制显示
        elif work_type == 'hospital':
            return 0

        # 学校点绘制显示
        elif work_type == 'school':
            return 0

        # 地铁点绘制显示
        elif work_type == 'subway':
            return 0

        # 公交车站点绘制
        elif work_type == 'bus':
            return 0

        # 购物中心点绘制
        elif work_type == 'shopping':
            return 0

        # 餐厅点绘制显示
        elif work_type == 'restaurant':
            return 0

        # 环境（公园）点绘制
        elif work_type == 'environment':
            return 0

        else:
            # 错误请求
            return 0

    else:
        return render_template('index.html', init_map=url_for('init_map'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=100, debug=True)
