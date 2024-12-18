import numpy as np
import matplotlib.pyplot as plt

# 参数定义
a = 12  # a >= b
b = 10  # b 的值
x_values = np.arange(1, b + 1)  # x 是大于 0 的整数，从 1 到 b

# 计算 y 的下界和上界
y_lower_bounds = a * x_values + np.floor((0 - a * x_values) / b) * b
y_upper_bounds = y_lower_bounds + b - 1

# 打印结果
print("x:", x_values)
print("y_lower_bound:", y_lower_bounds)
print("y_upper_bound:", y_upper_bounds)

# 绘制图形
plt.figure(figsize=(10, 5))
plt.plot(x_values, y_lower_bounds, marker='o', linestyle='-', color='blue', label='y_lower_bound')
plt.plot(x_values, y_upper_bounds, marker='o', linestyle='--', color='red', label='y_upper_bound')
plt.title('Plot of y bounds = ax + floor((0 - ax) / b) * b and y bounds = ax + floor((0 - ax) / b) * b + b - 1')
plt.xlabel('x')
plt.ylabel('y bounds')
plt.grid(True)
plt.legend()
plt.show()