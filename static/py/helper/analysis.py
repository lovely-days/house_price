# encoding:utf-8

import re


# 插值数据请求
# input: null
# output: 区域预测点网对应 json 数据

def interpolation():
    longitude = []
    latitude = []
    price = []

    file = open("../predict/data/price_interpolation.txt", 'r', encoding='utf-8')

    line = file.readline()
    while line:
        # print(line)
        ret_data = re.findall(r"([^,\n]+)", line)
        longitude.append(ret_data[0])
        latitude.append(ret_data[1])
        price.append(ret_data[2])

        return_json = {"longitude": longitude, "latitude": latitude, "price": price}
        return return_json

