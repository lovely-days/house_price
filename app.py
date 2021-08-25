# encoding:utf-8
from flask import Flask, url_for, redirect, request, jsonify
from flask import render_template

import re
import math
from collections import defaultdict
import tensorflow as tf
from geopy.distance import geodesic
import numpy as np

import src.static.py.helper.sql as db_helper
import src.static.py.helper.geojson as geojson_helper
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

        if work_type == "condition_select":

            json_return = geojson_helper.select_coordinate_geo(request_json)
            # print(request_json)
            return jsonify(json_return)

        if work_type == "house_predict":
            # 经度，纬度
            data_coordinate = request_json.pop("coordinates")

            infrastructure = defaultdict(list)
            mean = []
            std = []
            file = open("./static/py/predict/data/infra_factor.txt", 'r', encoding='utf-8')

            line = file.readline()
            while line:
                print(line)
                ret_data = re.findall(r"([^,\n]+)", line)
                if ret_data[0] == "mean":
                    for i in range(1, len(ret_data)):
                        mean.append(float(ret_data[i]))
                elif ret_data[0] == "std":
                    for i in range(1, len(ret_data)):
                        std.append(float(ret_data[i]))
                else:
                    price_factor = float(ret_data[3])
                    coordinates = [float(ret_data[1]), float(ret_data[2])]
                    infrastructure[ret_data[0]].append({"coordinates": coordinates, "price_factor": price_factor})
                line = file.readline()

            file.close()

            factors = []
            for key in infrastructure:
                count = 0
                factor = 0
                for item_infra in infrastructure[key]:
                    distance = geodesic((item_infra["coordinates"][1], item_infra["coordinates"][0]),
                                        (data_coordinate[1], data_coordinate[0])).km
                    # print(distance)
                    if distance < 3:
                        factor = factor + item_infra["price_factor"] / math.exp(distance)
                        count = count + 1
                if count == 0:
                    factor = 0
                else:
                    factor = factor / count
                factors.append(factor)

            dataset = np.array(factors)
            mean = np.array(mean)
            std = np.array(std)

            dataset = np.reshape(dataset, (1, 6))
            mean = np.reshape(mean, (1, 6))
            std = np.reshape(std, (1, 6))

            # 直接利用训练样本均值及均方差对待求数据极限归一化处理
            dataset -= mean
            dataset /= std

            # 模型加载
            model = tf.keras.models.load_model("./static/py/predict/model_19_339")
            # 模型预测值计算
            price_predict = model.predict(dataset[:])
            print(price_predict)

            json_return = {"predict": str(price_predict[0][0])}

            return jsonify(json_return)

        else:
            # 错误请求
            return 0



    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=100, debug=True)
