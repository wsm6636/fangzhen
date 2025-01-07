import matplotlib.pyplot as plt
import numpy as np

# 定义参数
a = 10  # a的值
b = 5   # b的值
max_x = 20  # x的最大值

# 计算两个表达式相等时的y值
ys = []
for x in range(max_x + 1):  # x从0到max_x
    # 由于方程是关于y的线性同余方程，我们可以解出y
    # (x-1)a - y ≡ y + ax (mod b)
    # 2y ≡ (x-1)a - ax (mod b)
    # 2y ≡ a(x-1-x) (mod b)
    # 2y ≡ -a (mod b)
    # y ≡ -a/2 (mod b)
    y = (-a // 2) % b
    ys.append(y)

# 绘制y值随x变化的图形
plt.plot(range(max_x + 1), ys, marker='o', linestyle='-', color='b')

# 添加图例和标签
plt.xlabel('x')
plt.ylabel('y')
plt.title('Intersection of ((x-1)a - y) mod b and (y + ax) mod b')
plt.grid(True)
plt.show()