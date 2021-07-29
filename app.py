# encoding:utf-8
from flask import Flask, url_for, redirect, request, jsonify
from flask import render_template

import re
from collections import defaultdict
import tensorflow as tf
from geopy.distance import geodesic
import numpy as np

import src.static.py.helper.sql as db_helper
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
        if work_type == "heat_map":
            sql = "select HouseID,Longitude,Latitude from houses"
            results = db_helper.select_all(sql)
            coordinates = []

            for result in results:
                coordinate = coordinate_helper.bd09_to_wgs84(float(result[1]), float(result[2]))
                coordinates.append({"type": "Feature", "properties": {},
                                    "geometry": {"type": "Point", "coordinates": coordinate}})

            json_return = {"type": "FeatureCollection", "features": coordinates}

            return jsonify(json_return)

        if work_type == "house_predict":
            # 经度，纬度
            data_coordinate = request_json.pop("coordinates")

            infrastructure = defaultdict(list)
            mean = std = 0
            file = open("./static/py/predict/data/infra_factor.txt", 'r', encoding='utf-8')

            line = file.readline()
            while line:
                print(line)
                ret_data = re.findall(r"([^,\n]+)", line)
                if ret_data[0] == "mean&std":
                    mean = ret_data[1]
                    std = ret_data[2]
                else:
                    price_factor = float(ret_data[3])
                    coordinates = [float(ret_data[1]), float(ret_data[2])]
                    infrastructure[ret_data[0]].append({"coordinates": [], "price_factor": price_factor})
                line = file.readline()

            file.close()

            baidu_coordinate = coordinate_helper.wgs84_to_bd09(data_coordinate[0], data_coordinate[1])

            factors = []
            for key in infrastructure:
                count = 0
                factor = 0
                for item_infra in infrastructure[key]:
                    distance = geodesic((item_infra["coordinates"][1], item_infra["coordinates"][0]),
                                        (baidu_coordinate[1], baidu_coordinate[0])).km
                    print(distance)
                    if distance < 3:
                        factor = factor + item_infra["price_factor"] / math.exp(distance)
                        count = count + 1
                if count == 0:
                    factor = 0
                else:
                    factor = factor / count
                factors.append(factor)
            # 模型加载
            model = tf.keras.models.load_model("./static/py/predict/model")
            # 模型预测值计算
            price_predict = model.predict(price_data)


        else:
            # 错误请求
            return 0

        '''
        # 操作类型判断
        if work_type == "data_show":
            # sql 语句判断
            sql = ""
            data_return = {}
            first_str = True

            if json_data["House"]:
                sql = "select * from houses"
                results = db_helper.select_all(sql)

                print(type(result))
                data_return["House"] = result

            for item in json_data:
                if first_str:
                    sql = sql + "'" + item + "'"
                    first_str = False
                else:
                    sql = sql + "," + "'" + item + "'"

            sql = "select * from infrastructures where `PointType` in (" + sql + ")"
            print(sql)

            response = {"status": True, "data manipulation": url_for('login')}
            return jsonify(response)

        else:
            # 错误请求
            return 0
        '''

    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=100, debug=True)
