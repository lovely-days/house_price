# encoding:utf-8

# 求解最佳迭代次数
# 绘制平均绝对误差与迭代次数关系图

from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np

# 数据加载
# dataset 为样本矩阵，包含对 6 大基础设施信息评值
# labels 为标签矩阵，包含单位房价数据
dataset = np.loadtxt('./dataset.txt', dtype=np.float, unpack=False, delimiter=',')
labels = np.loadtxt('./labels.txt', dtype=np.float, unpack=False, delimiter=',')

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
def build_model():
    keras_model = keras.Sequential()

    # 添加 8 个全连接层，每层 32 个神经元，激活采用 relu 函数
    for num in range(12):
        keras_model.add(keras.layers.Dense(32, activation='relu'))

    # 输出层，一个输出值，即单位房价数据
    keras_model.add(keras.layers.Dense(1))

    # 模型参数设置，损失函数采用平均绝对误差，优化选用 RMSprop 方法
    keras_model.compile(loss='mae', optimizer='rmsprop', metrics=['mae'])

    return keras_model


# epoch 参数确定

nums = 10
num_val_samples = int(len(dataset) / nums)
num_epochs = 500
all_mae_histories = []

for n in range(nums):
    print('processing fold #', n)

    # 依次把 k 分之一数据中的每一份作为校验数据集
    every_val_dataset = dataset[n * num_val_samples: (n + 1) * num_val_samples]
    every_val_labels = labels[n * num_val_samples: (n + 1) * num_val_samples]

    # 把剩下的 k-1 分之一数据作为训练数据,如果第 i 分数据作为校验数据，那么把前 i-1 份和第 i 份之后的数据连起来
    every_train_dataset = np.concatenate([dataset[: n * num_val_samples], dataset[(n + 1) * num_val_samples:]], axis=0)
    every_train_labels = np.concatenate([labels[: n * num_val_samples], labels[(n + 1) * num_val_samples:]], axis=0)

    # 模型创建
    print("build model")
    model = build_model()
    # 把分割好的训练数据和校验数据输入网络
    history = model.fit(every_train_dataset, every_train_labels, validation_data=(every_val_dataset, every_val_labels),
                        epochs=num_epochs, batch_size=32, verbose=1)
    mae_history = history.history['val_mae']
    all_mae_histories.append(mae_history)

    # print(model.evaluate(every_train_dataset, every_train_labels, batch_size=32))
    # print(model.predict(every_train_dataset, batch_size=32))


average_mae_history = [
    np.mean([x[i] for x in all_mae_histories]) for i in range(num_epochs)
]

# 各 epoch 平均绝对误差图像
plt.plot(range(1, len(average_mae_history) + 1), average_mae_history)
plt.xlabel('Epochs')
plt.ylabel('Validation MAE')
plt.show()
