# encoding:utf-8
from flask import Flask, url_for, redirect, request, jsonify
from flask import render_template

import src.static.py.helper.sql as db_helper
import src.static.py.helper.analysis as analysis_helper
import src.static.py.helper.graphic as graphic_helper
import src.static.py.helper.predict as predict_helper
import src.static.py.helper.retrieval as retrieval_helper
import src.static.py.helper.validate as validate_helper
import src.static.py.helper.co_system as coordinate_helper
from src.static.py.helper import config

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


@app.route('/index', methods=('POST', 'GET'))
def index():
    if request.method == "POST":
        request_json = request.get_json(force=True)
        work_type = request_json.pop("type")

        print(work_type)

        # 操作类型判断
        if work_type == "data_select":
            select_type = request_json["select_type"]
            condition = request_json["select_condition"]

            if select_type == 'Rectangle':
                json_return = graphic_helper.rectangle(condition)
            elif select_type == 'Circle':
                json_return = graphic_helper.circle(condition)
            elif select_type == 'Polygon':
                json_return = graphic_helper.polygon(condition)
            else:
                json_return = {"wrong"}

            return jsonify(json_return)

        if work_type == "condition_select":
            json_return = retrieval_helper.select_coordinate_geo(request_json)
            # print(request_json)
            return jsonify(json_return)

        if work_type == "data_analysis":
            analysis_type = request_json["analysis_type"]

            if analysis_type == "heat_map":
                json_return = analysis_helper.heat_map()
                return jsonify(json_return)

            if analysis_type == "predict_interpolation_map":
                json_return = analysis_helper.interpolation()
                return jsonify(json_return)

        if work_type == "house_predict":
            # 经度，纬度
            data_coordinate = request_json.pop("coordinates")
            json_return = predict_helper.price_predict(data_coordinate)

            return jsonify(json_return)

        else:
            # 错误请求
            return 0

    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=100, debug=True)
