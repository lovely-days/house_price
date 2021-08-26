# encoding:utf-8

import re
import math
from collections import defaultdict
import tensorflow as tf
from geopy.distance import geodesic
import numpy as np

import src.static.py.helper.co_system as coordinate_helper

all_price = []
infrastructure = defaultdict(list)
mean = []
std = []
file = open("./static/py/predict/data/infra_factor.txt", 'r', encoding='utf-8')

line = file.readline()
while line:
    # print(line)
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

# 117.052237,34.385425
# 117.342002,34.151637
#  经度 ，纬度
for longitude in range(117052, 117342, 3):
    for latitude in range(34151, 34385, 3):
        data_coordinate = coordinate_helper.gcj02_to_wgs84(float(longitude) / 1000, float(latitude) / 1000)

        print(data_coordinate)
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
            factors.append(float(factor))

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
        predict_price = model.predict(dataset[:])
        print(predict_price)

        all_price.append([data_coordinate[0], data_coordinate[1], predict_price[0][0]])

all_price = np.array(all_price)
np.savetxt('./data.txt', all_price, fmt='%.18f', delimiter=',')