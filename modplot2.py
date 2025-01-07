import matplotlib.pyplot as plt
import numpy as np

# 定义参数
a = 10  # a的值
b = 3   # b的值
max_x = 50  # x的最大值

# 初始化列表来存储所有的点
x_values = []
m1_n2_values = []
n1_m2_values = []

# 遍历x的值
for x in range(max_x + 1):
    # 计算-2ax mod b
    delta = (-2 * a * x) % b
    print(f"For x = {x}:")
    # 对于每个可能的m1 - n2，计算对应的n1 - m2
    for m1_n2 in range(b):  # m1 - n2的可能值
        n1_m2 = (m1_n2 - delta) % b  # 计算对应的n1 - m2
        if m1_n2 >= n1_m2:  # 确保m1 - m2 >= n1 - n2
            print(f"  m1 - n2 = {m1_n2}, n1 - m2 = {n1_m2}")
            x_values.append(x)
            m1_n2_values.append(m1_n2)
            n1_m2_values.append(n1_m2)

# 绘制所有点
plt.figure(figsize=(12, 6))
plt.scatter(x_values, m1_n2_values, c='blue', label='m1 - n2', alpha=0.5)
plt.scatter(x_values, n1_m2_values, c='red', label='n1 - m2', alpha=0.5,marker='x',)

# 添加图例和标签
plt.legend()
plt.xlabel('x')
plt.ylabel('Values of m1 - n2 and n1 - m2')
plt.title('All possible points for m1 - n2 and n1 - m2 with x as the horizontal axis')
plt.grid(True)
plt.show()