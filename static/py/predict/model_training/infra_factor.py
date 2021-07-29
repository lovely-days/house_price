# encoding:utf-8
import math

from collections import defaultdict
from geopy.distance import geodesic

import src.static.py.helper.sql as db_helper

# mysql
sql_house = "select * from houses"
sql_infrastructure = "select * from infrastructures"
db_house = db_helper.select_all(sql_house)
db_infrastructure = db_helper.select_all(sql_infrastructure)

'''
for item in db_house:
    for element in range(len(item)):
        print(element)
        print(item[element])

for item in db_infrastructure:
    for element in range(len(item)):
        print(element)
        print(item[element])
'''

# infrastructure = {"House": [], "Hospital": [], "School": [], "Environment": [], "Subway": [], "BusStation": [], "Shopping": []}

infrastructure = defaultdict(list)
house_coordinates = []
house_factors = []
house_labels = []

for item in db_infrastructure:
    price_factor = 0
    coordinates = [float(item[3]), float(item[4])]
    infrastructure[item[2]].append({"coordinates": coordinates, "price_factor": price_factor})

for item in db_house:
    unit_price = float(item[3])
    coordinates = [float(item[12]), float(item[13])]
    house_labels.append(unit_price)
    house_coordinates.append({"coordinates": coordinates, "unit_price": unit_price})

m = 0
# 遍历所有房价数据，根据距离加权求出各基础设施要素影响因子
# 距离影响极限取4km, 采用指数处理非线性化距离因子
for key in infrastructure:
    for item_infra in infrastructure[key]:
        count = 0
        for item_house in house_coordinates:
            distance = geodesic((item_infra["coordinates"][1], item_infra["coordinates"][0]),
                                (item_house["coordinates"][1], item_house["coordinates"][0])).km
            print(distance)
            if distance < 4:
                item_infra["price_factor"] = item_infra["price_factor"] + item_house["unit_price"] / math.exp(distance)
                count = count + 1
        if count == 0:
            price_factor = 0
        else:

            item_infra["price_factor"] = item_infra["price_factor"] / count

# 设施要素影响因子矩阵存储
file = open('../data/infra_factor.txt', 'a', encoding='utf-8')
for key in infrastructure:
    for item_infra in infrastructure[key]:
        infra_str = key + ',' + str(item_infra["coordinates"][0]) + ',' + str(item_infra["coordinates"][1]) + ',' + str(item_infra["price_factor"]) + '\n'
        print(infra_str)
        file.writelines(infra_str)

file.close()


