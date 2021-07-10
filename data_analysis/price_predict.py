from random import random

from tensorflow import keras

from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import pymysql
import re

# mysql
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

mean = np.mean(datas, axis=0)
datas -= mean
std = np.std(datas, axis=0)
datas /= std

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

#        val_datas[rows, column] -= mean
#        val_datas[rows, column] /= std

for rows in range(len(labels)):
    for column in range(len(labels[rows])):
        print(labels[rows, column])

for rows in range(len(datas)):
    for column in range(len(datas[rows])):
        print("############"+str(column))
        print(datas[rows, column])

for rows in range(len(val_labels)):
    for column in range(len(val_labels[rows])):
        print(val_labels[rows, column])

print(len(val_labels))

for rows in range(len(val_datas)):
    for column in range(len(val_datas[rows])):
        print("************"+str(column))
        print(val_datas[rows, column])

print(len(val_datas))
print(123141231231231231231)

'''
def build_model():
    model = keras.Sequential()

    # Adds a densely-connected layer with 64 units to the model:
    model.add(keras.layers.Dense(64, activation='relu'))
    # Add another:
    model.add(keras.layers.Dense(64, activation='relu'))
    # Add a softmax layer with 1 output units:
    model.add(keras.layers.Dense(1, activation='softmax'))

    model.compile(loss='mae', optimizer='rmsprop', metrics=['mae'])

    return model


nums = 10
num_val_samples = len(datas) // nums
num_epochs = 30
all_mae_histories = []

for n in range(10):
    print('processing fold #', n)

    # 依次把 k 分之一数据中的每一份作为校验数据集
    every_val_data = datas[n * num_val_samples: (n + 1) * num_val_samples]
    every_val_labels = labels[n * num_val_samples: (n + 1) * num_val_samples]

    # 把剩下的 k-1 分之一数据作为训练数据,如果第 i 分数据作为校验数据，那么把前 i-1 份和第 i 份之后的数据连起来
    every_train_data = np.concatenate([datas[: n * num_val_samples], datas[(n + 1) * num_val_samples:]], axis=0)
    every_train_labels = np.concatenate([labels[: n * num_val_samples], labels[(n + 1) * num_val_samples:]], axis=0)

    # 模型创建
    print("build model")
    model = build_model()

    # 把分割好的训练数据和校验数据输入网络
    history = model.fit(every_train_data, every_train_labels, validation_data=(every_val_data, every_val_labels),
                        epochs=num_epochs, batch_size=1, verbose=0)
    mae_history = history.history['val_mae']
    all_mae_histories.append(mae_history)

    print(model.evaluate(every_train_data, every_train_labels, batch_size=32))
    print(model.predict(every_train_data, batch_size=32))

average_mae_history = [
    np.mean([x[i] for x in all_mae_histories]) for i in range(num_epochs)
]

plt.plot(range(1, len(average_mae_history) + 1), average_mae_history)
plt.xlabel('Epochs')
plt.ylabel('Validation MAE')
plt.show()


'''

model = keras.Sequential()

# Adds a densely-connected layer with 64 units to the model:
model.add(keras.layers.Dense(64, activation='relu'))
# Add another:
model.add(keras.layers.Dense(64, activation='relu'))
# Add a softmax layer with 1 output units:
model.add(keras.layers.Dense(1))

model.compile(loss='mae', optimizer='rmsprop', metrics=['mae'])

num_epochs = 500
all_mae_histories = []

history = model.fit(datas, labels, validation_data=(val_datas, val_labels), epochs=num_epochs, batch_size=32, verbose=0)
print(history.history.keys())
mae_history = history.history['val_mae']

val_mse, val_mae = model.evaluate(val_datas, val_labels, batch_size=32)
val_predict = model.predict(val_datas, batch_size=32)

print("val_mse: {}  val_mae: {}".format(val_mse, val_mae))

plt.plot(range(1, len(mae_history) + 1), mae_history[:])
plt.xlabel('Epochs')
plt.ylabel('Validation MAE')
plt.show()


plt.scatter(val_labels[:], val_predict[:])
plt.plot([0, 1000], [0, 1000], 'r', label=' y=x')
plt.xlabel('true value')
plt.ylabel('predict value')
plt.legend()
plt.show()





