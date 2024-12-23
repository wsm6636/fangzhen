import numpy as np

# 参数定义
a = 12  # a >= b
b = 10  # b 的值
x_values = np.arange(1, 20, 1)  # x 是大于 0 的整数，从 1 到 b

# 计算 y 的范围
y_lower_bounds = -np.floor((-a * x_values) / b) * b - (a - b) - a * x_values
y_upper_bounds = -np.floor((-a * x_values) / b) * b - a * x_values

# 打印结果
print("x:", x_values)
print("y_lower_bound:", y_lower_bounds)
print("y_upper_bound:", y_upper_bounds)

# 绘制图形
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
plt.plot(x_values, y_lower_bounds, marker='o', linestyle='-', color='blue', label='y_lower_bound')
plt.plot(x_values, y_upper_bounds, marker='o', linestyle='--', color='red', label='y_upper_bound')
plt.title('Plot of y bounds = -k*b - (a - b) - ax and y bounds = -k*b - ax')
plt.xlabel('x')
plt.ylabel('y bounds')
plt.grid(True)
plt.legend()
plt.show()