# encoding:utf-8

from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import pymysql
import re

# mysql
from sklearn.linear_model import LinearRegression

db = pymysql.connect(host='localhost', user='root', password='ZyW106509', database='webgis_design')
cursor = db.cursor()
sql = "select * from houses"
cursor.execute(sql)
results = cursor.fetchall()
db.close()

# houses = []           房价   单价   朝向   楼层   房屋类型/装修情况   小区....
#                       区域/细一级区域   面积   房间类型...  卧室数目  厅数目  建筑年龄   经度    纬度
#                       "HousePrice", "priceSquare", "direction", "floor", "HouseType","Community"
#                       "region", "area", "RoomType", "livingroom", "halls" "years", "lon", "lat"

datas = []
labels = []

# val_datas = []
# val_labels = []

# for result in results:
#     for element in range(len(result)):
#         print(element)
#         print(result[element])

dic_direction = defaultdict(list)
dic_floor = defaultdict(list)
dic_HouseType = defaultdict(list)
dic_region = defaultdict(list)
dic_RoomType = defaultdict(list)
dic_Community = defaultdict(list)
array_Years = []

for result in results:

    # direction
    dic_direction[result[6]].append(float(result[2]))
    print(result[6])

    # floor
    dic_floor[result[5]].append(float(result[2]))
    print(result[5])

    # HouseType
    dic_HouseType[result[7]].append(float(result[2]))
    print(result[7])

    # Region
    dic_region[result[11]].append(float(result[2]))
    print(result[11])

    # RoomType
    # dic_RoomType[result[4]].append(float(result[2]))
    # print(result[4])

    # Community
    # dic_Community[result[10]].append(float(result[2]))
    # print(result[10])

    # Years
    ret_space = re.findall(r"\d{4}", result[9])
    if len(ret_space) == 0:
        print(result[8])
        print(0)
        continue
    else:
        array_Years.append(int(ret_space[0]))
        print(ret_space[0])

for result in results:
    # HousePrice
    # output
    label = [float(result[2])]

    # influence factor
    # input
    data = []

    # direction
    data.append(np.percentile(dic_direction[result[6]], 50))

    # floor
    data.append(np.percentile(dic_floor[result[5]], 50))

    # HouseType
    data.append(np.percentile(dic_HouseType[result[7]], 50))

    # Community
    # data.append(np.percentile(dic_region[result[10]], 50))
    # data.append(0)

    # region
    data.append(np.percentile(dic_region[result[11]], 50))

    # area
    ret_area = re.findall(r"((\d*[.]\d*)|(\d*))", result[8])[0][0]
    data.append(float(ret_area))
    # print(ret_space)

    # RoomType
    # data.append(np.percentile(dic_region[result[4]], 50))
    # data.append(0)

    # livingroom halls
    ret_rooms = re.findall(r"\d", result[4])
    if len(ret_rooms) == 0:
        continue
    else:
        data.append(int(ret_rooms[0]))
        data.append(int(ret_rooms[1]))

    # Years
    ret_Years = re.findall(r"\d{4}", result[9])
    if len(ret_Years) == 0:
        data.append(2021 - np.percentile(array_Years, 50))
    else:
        data.append(2021 - int(ret_Years[0]))
    # print(ret_space)

    print(label)

    for element in range(len(data)):
        print(data[element])
        print("###########" + str(element))

    labels.append(label)
    datas.append(data)

print(1231231243415234)

# 1/10 数据作为检验数据集
# val_data val_label
# for element in range(len(labels)):
#    if element % 10 == 6:
#        val_labels.append(labels[element])
#        val_datas.append(datas[element])


# 卷积神经网络输入数据归一化处理
datas = np.array(datas)
labels = np.array(labels)

# mean = np.mean(datas, axis=0)
# datas -= mean
# std = np.std(datas, axis=0)
# datas /= std

val_datas = []
val_labels = []

for row in range(1, len(datas)):
    if row % 10 == 3:
        val_datas.append(datas[row])
        val_labels.append(labels[row])
        # np.append(val_datas, datas[row])
        # np.append(val_labels, labels[row])
        np.delete(datas, row)
        np.delete(labels, row)

val_datas = np.array(val_datas)
val_labels = np.array(val_labels)

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

houses = ["朝向", "楼层", "房屋情况", "区域", "面积", "卧室数目", "厅数目", "建筑年龄"]

for n in range(len(datas)):
    print("##############")
    print(datas[n, 0])

for n in range(4):
    plt.subplot(2, 2, n+1)
    plt.scatter(datas[:, n], labels)
    plt.xlabel(houses[n])
    plt.ylabel("房价")

    # lin_reg = LinearRegression()
    # lin_reg.fit(datas[:, n], labels)

    # y_predict = lin_reg.predict(datas[:, n])

    # plt.plot(datas[:, n], y_predict, 'r')
    # plt.legend()

plt.show()

for n in range(4, 8):
    plt.subplot(2, 2, n-3)
    plt.scatter(datas[:, n], labels)
    plt.xlabel(houses[n])
    plt.ylabel("房价")

    # lin_reg = LinearRegression()
    # lin_reg.fit(datas[:, n], labels)

    # y_predict = lin_reg.predict(datas[:, n])

    # plt.plot(datas[:, n], y_predict, 'r')
    # plt.legend()

plt.show()
