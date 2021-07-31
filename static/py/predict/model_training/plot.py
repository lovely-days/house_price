# encoding:utf-8

import matplotlib.pyplot as plt
import numpy as np

validate = np.loadtxt('../data/val_loss.txt', dtype=np.float, unpack=False, delimiter=',')
test = np.loadtxt('../data/test_loss.txt', dtype=np.float, unpack=False, delimiter=',')

# 各 layers 平均绝对误差图像
plt.plot(test[:, 0], test[:, 2], label='test loss (epoch=200)')
plt.plot(validate[:, 0], validate[:, 2], label='validate loss (epoch=200)')
plt.legend(loc='upper right')
plt.xticks(range(2, 24, 2))
plt.xlabel('Layers')
plt.ylabel('Model MAE')
plt.show()


validate_epoch = np.loadtxt('../data/val_loss_epoch.txt', dtype=np.float, unpack=False, delimiter=',')
test_epoch = np.loadtxt('../data/test_loss_epoch.txt', dtype=np.float, unpack=False, delimiter=',')

# 各 epoch 平均绝对误差图像
plt.plot(test_epoch[:, 1], test_epoch[:, 2], label='test loss (layers = 19 )')
plt.plot(validate_epoch[:, 1], validate_epoch[:, 2], label='validate loss (layers = 19 )')
plt.legend(loc='upper right')
plt.xticks(range(0, 410, 50))
plt.xlabel('Epochs')
plt.ylabel('Model MAE')
plt.show()

