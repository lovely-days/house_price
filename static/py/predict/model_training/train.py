# encoding:utf-8

import os

from tensorflow import keras
import numpy as np

# 模型训练

# 数据加载
# dataset 为样本矩阵，包含对 6 大基础设施评值
# labels 为标签矩阵，包含单位房价数据
dataset = np.loadtxt('../data/dataset.txt', dtype=np.float, unpack=False, delimiter=',')
labels = np.loadtxt('../data/labels.txt', dtype=np.float, unpack=False, delimiter=',')

# 1/10 数据用作检验数据集
test_dataset = []
test_labels = []

temp_dataset = []
temp_labels = []

for row in range(len(dataset)):
    if row % 10 == 3:
        test_dataset.append(dataset[row])
        test_labels.append(labels[row])
    else:
        temp_dataset.append(dataset[row])
        temp_labels.append(labels[row])

test_dataset = np.array(test_dataset)
test_labels = np.array(test_labels)

dataset = np.array(temp_dataset)
labels = np.array(temp_labels)

# 输出测试
'''
for row in range(len(labels)):
    print(labels[row])

for row in range(len(dataset)):
    for column in range(len(dataset[row])):
        print("############"+str(column))
        print(dataset[row, column])

for row in range(len(val_labels)):
    print(val_labels[row])

for row in range(len(val_dataset)):
    for column in range(len(val_dataset[row])):
        print("************"+str(column))
        print(val_dataset[row, column])
'''


# 深度神经网络构建
def build_model(layers):
    keras_model = keras.Sequential()

    # 添加 8 个全连接层，每层 32 个神经元，激活采用 relu 函数
    for num in range(layers):
        keras_model.add(keras.layers.Dense(32, activation='relu'))

    # 输出层，一个输出值，即单位房价数据
    keras_model.add(keras.layers.Dense(1))

    # 模型参数设置，损失函数采用平均绝对误差，优化选用 RMSprop 方法
    keras_model.compile(loss='mae', optimizer='rmsprop', metrics=['mae'])

    return keras_model


loss_all = []
validate_loss_all = []

# 模型层数
for layer_num in range(19, 20, 1):

    # 模型构建
    print("build model")
    model = build_model(layer_num)

    nums = 10
    num_val_samples = int(len(dataset) / nums)
    epochs_step = 1
    min_loss = 1800

    # 训练迭代次数
    for num_epochs in range(1, 400):

        print("layers" + str(layer_num) + "num_epochs" + str(num_epochs))

        loss_sum = 0
        mae_sum = 0

        # k 分训练法
        for n in range(nums):
            print('processing fold #', n)

            # 依次把 k 分之一数据中的每一份作为校验数据集
            every_val_dataset = dataset[n * num_val_samples: (n + 1) * num_val_samples]
            every_val_labels = labels[n * num_val_samples: (n + 1) * num_val_samples]

            # 把剩下的 k-1 分之一数据作为训练数据,如果第 i 分数据作为校验数据，那么把前 i-1 份和第 i 份之后的数据连起来
            every_train_dataset = np.concatenate([dataset[: n * num_val_samples], dataset[(n + 1) * num_val_samples:]],
                                                 axis=0)
            every_train_labels = np.concatenate([labels[: n * num_val_samples], labels[(n + 1) * num_val_samples:]],
                                                axis=0)

            # 把分割好的训练数据和校验数据输入网络
            model.fit(every_train_dataset, every_train_labels, epochs=epochs_step, batch_size=32, verbose=1)

            validate = model.evaluate(every_val_dataset, every_val_labels, batch_size=32)
            loss_sum = loss_sum + validate[0]
            mae_sum = mae_sum + validate[1]

        validate_loss_all.append([layer_num, num_epochs, loss_sum/nums, mae_sum/nums])

        test = model.evaluate(test_dataset, test_labels, batch_size=32)
        loss_all.append([layer_num, num_epochs, test[0], test[1]])

        # 较小损失值模型保存
        if test[0] < min_loss:
            min_loss = test[0]
            # 模型保存
            checkpoint_path = "../model_" + str(layer_num) + "_" + str(num_epochs)
            print(checkpoint_path)
            checkpoint_dir = os.path.dirname(checkpoint_path)

            cp_callback = keras.callbacks.ModelCheckpoint(filepath=checkpoint_path, verbose=1, save_weights_only=True,
                                                          period=5)
            model.save(checkpoint_path)


validate_loss_all = np.array(validate_loss_all)
np.savetxt('../data/val_loss_epoch.txt', validate_loss_all, fmt='%.18f', delimiter=',')

loss_all = np.array(loss_all)
np.savetxt('../data/test_loss_epoch.txt', loss_all, fmt='%.18f', delimiter=',')

