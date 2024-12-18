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

# 绘制五角星的顶点
def star(R):
    # 五角星的五个顶点
    theta = np.linspace(0, 2 * np.pi, 10, endpoint=False)
    outer = R * np.cos(theta)
    inner = R * np.cos(theta + np.pi / 5)
    top = R * np.sin(theta)
    bottom = R * np.sin(theta + np.pi / 5)
    # 将内外点交替连接形成五角星
    star_points_x = np.concatenate((outer, inner[1:-1][::-1]))
    star_points_y = np.concatenate((top, bottom[1:-1][::-1]))
    return star_points_x, star_points_y

# 生成五角星的顶点
R = 1  # 五角星的半径
x_star, y_star = star(R)

# 绘制图形
plt.figure(figsize=(10, 10))
plt.plot(x_star, y_star, 'k-', lw=2, label='Pentagram Outline')

# 将 y3 的交集区域映射到五角星的顶点上
# 这里我们使用颜色来表示 y3 的值
y3_values = np.random.uniform(y3_lower_bounds[0], y3_upper_bounds[0], len(x_star))

# 绘制五角星内部的点
plt.scatter(x_star, y_star, c=y3_values, cmap='viridis', alpha=0.7, label='y3 Region')

plt.title('y3 Intersection Region in a Pentagram')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.show()