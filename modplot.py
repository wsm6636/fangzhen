import numpy as np
import matplotlib.pyplot as plt

# 参数
m = 3 # 0 <= m <= b
n = 5
a = 12  # a >= b
b = 10

# 创建x值的数组，x是大于0的整数
x_values = np.arange(1, 50, 1)

# 计算(m - ax) mod b的结果
y_values = (m - a * x_values) % b
y_values1 = (n + a * x_values) % b

print(y_values)
print(y_values1)
# 绘制周期性波形图
# plt.figure(figsize=(10, 5))
# plt.plot(x_values, y_values, marker='o', linestyle='-')
# plt.title('Waveform Plot of (m - ax) mod b')
# plt.xlabel('x')
# plt.ylabel('(m - ax) mod b')
# plt.grid(True)
# plt.xticks(x_values)  # 设置x轴刻度为x_values中的整数
# plt.show()

# 创建一个图形窗口，并将其分为1行2列的子图布局
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# 在第一个子图上绘图
ax1.plot(x_values, y_values, marker='o', linestyle='-')
ax1.set_title('(m - ax) mod b')
ax1.set_xlabel('x')
ax1.grid(True)
ax1.set_xticks(x_values)  # 设置x轴刻度为x_values中的整数
# 在第二个子图上绘图
ax2.plot(x_values, y_values1, marker='o', linestyle='-')
ax2.set_title('(n + ax) mod b')
ax2.set_xlabel('x')
ax2.grid(True)

ax2.set_xticks(x_values)  # 设置x轴刻度为x_values中的整数
# 显示图形
plt.show()