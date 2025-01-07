import matplotlib.pyplot as plt
import numpy as np

# 定义参数
T1 = 10  # T1的值
T2 = 7   # T2的值
max_j = 20  # j的最大值

# 初始化列表来存储所有的点
y1_values = []
y2_values = []
n_values = []
j_values = []
y1_y2_diff_values = []

# 打开文件用于写入
with open('mod.txt', 'w') as file:
    # 遍历j的值
    for j in range(max_j + 1):
        # 计算r
        r = (j * T1) % T2
        # 生成y2的值
        for y2 in range(T2):
            # 计算y1
            y1 = (y2 - 2 * r) % T2
            # 计算n的值范围
            n_min = (j * T1 - y2) // T2
            if n_min < 0:
                n_min = 0
            n_max = (j * T1 + y1 + T2) // T2
            
            m1 = (j * T1 + y1) % T2
            m2 = (y2 - j * T1) % T2

            # 计算y1 - y2
            y1_y2_diff = y1 - y2

            # 添加到列表中
            y1_values.append(y1)
            y2_values.append(y2)
            n_values.append(n_min)
            j_values.append(j)
            y1_y2_diff_values.append(y1_y2_diff)

            # print(f"j = {j}, y1 = {y1}, y2 = {y2}, n_min = {n_min},  y1 - y2 = {y1-y2}")
            # 写入结果到文件
            file.write(f"j = {j}, y1 = {y1}, y2 = {y2}, n_min = {n_min},  y1 - y2 = {y1-y2}, r = {r}, m1 = {m1}, m2={m2}\n")
        file.write("\n")



# 绘制图形
fig, axs = plt.subplots(3, 1, figsize=(10, 12))

# 绘制y1和y2
for j in range(max_j + 1):
    idx = [i for i, val in enumerate(j_values) if val == j]
    axs[0].scatter([y2_values[i] for i in idx], [y1_values[i] for i in idx], label=f'j={j}')

axs[0].set_xlabel('y2')
axs[0].set_ylabel('y1')
axs[0].set_title('y1 vs y2 for different j')
axs[0].legend()
axs[0].grid(True)

# 绘制n的值
for j in range(max_j + 1):
    idx = [i for i, val in enumerate(j_values) if val == j]
    axs[1].scatter([j_values[i] for i in idx], [n_values[i] for i in idx], label=f'j={j}')

axs[1].set_xlabel('j')
axs[1].set_ylabel('n')
axs[1].set_title('n vs j for different y2')
axs[1].legend()
axs[1].grid(True)

# 绘制y1-y2的值
for j in range(max_j + 1):
    idx = [i for i, val in enumerate(j_values) if val == j]
    axs[2].scatter([j_values[i] for i in idx], [y1_y2_diff_values[i] for i in idx], label=f'j={j}')

axs[2].set_xlabel('y1_y2')
axs[2].set_ylabel('n')
axs[2].set_title('n vs y1_y2 for different y2')
axs[2].legend()
axs[2].grid(True)

plt.tight_layout()
plt.show()