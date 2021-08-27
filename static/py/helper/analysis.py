# encoding:utf-8

import re

import src.static.py.helper.sql as db_helper
import src.static.py.helper.co_system as coordinate_helper


# 插值数据请求
# input: null
# output: 区域预测点网对应 json 数据

def interpolation():
    longitude = []
    latitude = []
    price = []

    file = open("../src/static/py/predict/data/price_interpolation.txt", 'r', encoding='utf-8')

    line = file.readline()
    while line:
        # print(line)
        ret_data = re.findall(r"([^,\n]+)", line)
        longitude.append(ret_data[0])
        latitude.append(ret_data[1])
        price.append(ret_data[2])

        line = file.readline()

    max_longitude = max(longitude)
    min_longitude = min(longitude)
    max_latitude = max(latitude)
    min_latitude = min(latitude)

    return_json = {"longitude": longitude, "latitude": latitude, "price": price,
                   "mum": [[min_longitude, min_latitude], [min_longitude, max_latitude],
                           [max_longitude, max_latitude], [max_longitude, min_latitude]]}

    return return_json


# 热力图数据请求
# input: null
# output: 绘制热力图所需房价点对应 json 格式数据

def heat_map():
    sql = "select HouseID,Longitude,Latitude from houses"
    results = db_helper.select_all(sql)
    coordinates = []

    for result in results:
        coordinate = coordinate_helper.bd09_to_wgs84(float(result[1]), float(result[2]))
        coordinates.append({"type": "Feature", "properties": {},
                            "geometry": {"type": "Point", "coordinates": coordinate}})

    json_return = {"type": "FeatureCollection", "features": coordinates}

    return json_return

