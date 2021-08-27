# encoding:utf-8

# 返会区域内一定步长点网预测房价数据
# 用于预测房价插值使用

import re
import math
from collections import defaultdict
import tensorflow as tf
from geopy.distance import geodesic
import numpy as np

import src.static.py.helper.co_system as coordinate_helper

infrastructure = defaultdict(list)
mean = []
std = []
file = open("../data/infra_factor.txt", 'r', encoding='utf-8')

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

for longitude in range(11705, 11734, 2):
    for latitude in range(3415, 3438, 2):
        data_coordinate = coordinate_helper.gcj02_to_wgs84(float(longitude) / 100, float(latitude) / 100)

        print(data_coordinate)
        print([longitude, latitude])
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
        model = tf.keras.models.load_model("../model_19_339")
        # 模型预测值计算
        predict_price = model.predict(dataset[:])
        print(predict_price)

        file_data = open('./price_interpolation.txt', 'a', encoding='utf-8')
        file_data.writelines(str(data_coordinate[0]) + ',' + str(data_coordinate[1]) + ',' + str(predict_price[0][0]) + '\n')
        file_data.close()
