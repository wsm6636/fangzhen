import numpy as np
import matplotlib.pyplot as plt

# 参数定义
a = 12  # a >= b
b = 10  # b 的值
x_values = np.arange(1, 20, 1)  # x 是大于 0 的整数，从 1 到 19

# 计算 y1 的下界和上界
k1 = np.floor((-a * x_values) / b)
y1_lower_bounds = -k1 * b - (a - b) - a * x_values
y1_upper_bounds = -k1 * b - a * x_values

# 计算 y2 的下界和上界
k2 = np.floor((-a * x_values) / b)
y2_lower_bounds = a * x_values + k2 * b
y2_upper_bounds = y2_lower_bounds + b - 1

# 找到两个图形的交集
y3_lower_bounds = np.maximum(y1_lower_bounds, y2_lower_bounds)
y3_upper_bounds = np.minimum(y1_upper_bounds, y2_upper_bounds)

# 过滤出有效的交集区间
valid_intersect = (y3_lower_bounds <= y3_upper_bounds)

# 打印结果
print("x:", x_values)
print("y1_lower_bound:", y1_lower_bounds)
print("y1_upper_bound:", y1_upper_bounds)
print("y2_lower_bound:", y2_lower_bounds)
print("y2_upper_bound:", y2_upper_bounds)
print("y3_lower_bound:", y3_lower_bounds)
print("y3_upper_bound:", y3_upper_bounds)

# 绘制图形
plt.figure(figsize=(10, 5))

# 绘制 y1 的界限
plt.plot(x_values, y1_lower_bounds, label='y1_lower_bound', color='blue', linestyle='-')
plt.plot(x_values, y1_upper_bounds, label='y1_upper_bound', color='blue', linestyle='--')

# 绘制 y2 的界限
plt.plot(x_values, y2_lower_bounds, label='y2_lower_bound', color='red', linestyle='-')
plt.plot(x_values, y2_upper_bounds, label='y2_upper_bound', color='red', linestyle='--')

# 绘制 y3 的界限
plt.fill_between(x_values[valid_intersect], y3_lower_bounds[valid_intersect], y3_upper_bounds[valid_intersect], color='green', alpha=0.5, label='y3_bounds')

plt.title('Plot of y1, y2 bounds and their intersection y3')
plt.xlabel('x')
plt.ylabel('y bounds')
plt.grid(True)
plt.legend()
plt.show()