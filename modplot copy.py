import numpy as np
import matplotlib.pyplot as plt

# 参数
m = 5  # 0 <= m <= b
a = 12  # a >= b
b = 10

# 创建x值的数组，x是大于0的整数
x_values = np.arange(1, 51, 1)

# 计算(m - ax) mod b的结果
y_values = (m - a * x_values) % b

num_sides = 5

# 多边形的参数方程
def polygon(t, R, num_sides):
    theta = 2 * np.pi / num_sides
    x = R * np.sin(theta * t)
    y = R * np.cos(theta * t)
    return x, y

# 生成多边形的顶点
t_values = np.arange(0, num_sides, 1)
R = 1  # 多边形的半径
x_polygon, y_polygon = polygon(t_values, R, num_sides)

# 绘制多边形
fig, ax = plt.subplots()
ax.plot(x_polygon, y_polygon, 'k--', lw=1)  # 绘制多边形的轮廓

# 将y_values映射到多边形的顶点上
# 这里我们使用颜色来表示y_values的值
colors = y_values / float(max(y_values))  # 归一化颜色值
sc = ax.scatter(x_polygon, y_polygon, c=colors, s=50, cmap='viridis', alpha=0.7)

# 添加颜色条
fig.colorbar(sc, ax=ax)

plt.title(f'Star Plot of (m - ax) mod b with {num_sides} sides')
plt.axis('equal')  # 保持x和y轴的比例一致
plt.show()