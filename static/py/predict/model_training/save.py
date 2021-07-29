# encoding:utf-8

# 模型保存测试
# 模型再次评估及预测值真值拟合分析

import tensorflow as tf
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

# 模型加载
model = tf.keras.models.load_model("../model")

# 模型评估
print(model.evaluate(test_dataset, test_labels, batch_size=32))

# 模型预测值计算
test_predict = model.predict(test_dataset, batch_size=32)

# 预测值与真值拟合分析
plt.scatter(test_labels[:], test_predict[:])
plt.plot([0, 40000], [0, 40000], 'r', label=' y=x')
plt.xlabel('true value')
plt.ylabel('predict value')
plt.legend()
plt.show()

