# encoding:utf-8

# 训练数据集生成
# dataset.txt 训练样本矩阵
# labels.txt 训练标记矩阵

import numpy as np
import math

from collections import defaultdict
from geopy.distance import geodesic

import src.static.py.helper.co_system as coordinate_helper
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
    coordinates = coordinate_helper.gcj02_to_wgs84(float(item[3]), float(item[4]))
    infrastructure[item[2]].append({"coordinates": coordinates, "price_factor": price_factor})

for item in db_house:
    unit_price = float(item[3])
    coordinates = coordinate_helper.bd09_to_wgs84(float(item[12]), float(item[13]))
    house_labels.append(unit_price)
    house_coordinates.append({"coordinates": coordinates, "unit_price": unit_price})

m = 0
# 遍历所有房价数据，根据距离加权求出各基础设施要素影响因子
# 距离影响极限取4km, 采用指数处理非线性化距离因子
for key in infrastructure:
    for item_infra in infrastructure[key]:
        print("#########################" + str(m))
        m = m + 1
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

m = 0
# 根据各基础设施要素影响因子反求房价影响因素矩阵
# 距离加权，距离因子指数非线性化，影响极限取3km
for item_house in house_coordinates:
    print("#########################" + str(m))
    m = m + 1
    factors = []
    for key in infrastructure:
        count = 0
        factor = 0
        for item_infra in infrastructure[key]:
            distance = geodesic((item_infra["coordinates"][1], item_infra["coordinates"][0]),
                                (item_house["coordinates"][1], item_house["coordinates"][0])).km
            print(distance)
            if distance < 3:
                factor = factor + item_infra["price_factor"] / math.exp(distance)
                count = count + 1
        if count == 0:
            factor = 0
        else:
            factor = factor / count
        factors.append(factor)
    house_factors.append(factors)

# 输入数据归一化处理
dataset = np.array(house_factors)
labels = np.array(house_labels)

mean = np.mean(dataset, axis=0)
dataset -= mean
std = np.std(dataset, axis=0)
dataset /= std

# 训练数据集文件保存
np.savetxt('../data/dataset.txt', dataset, fmt='%.18f', delimiter=',')
np.savetxt('../data/labels.txt', labels, fmt='%.18f', delimiter=',')

print("mean: ")
print(mean)
print("std: ")
print(std)

