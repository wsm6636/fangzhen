import matplotlib.pyplot as plt
import sys

# 读取文件并解析数据
def read_data(file_path):
    timestamps = {}
    pp_timestamps = []
    parsing_pp_timestamps = False
    with open(file_path, 'r') as file:
        lines = file.readlines()

    current_name = None
    for line in lines:
        line = line.strip()
        if line.startswith('### '):
            current_name = line.split('###')[1].strip()
            timestamps[current_name] = {'read_times': [], 'execution_times': []}
        elif current_name and 'read       time:' in line:
            timestamps[current_name]['read_times'] = list(map(float, line.split(':')[1].split()))
        elif current_name and 'Execution times:' in line:
            timestamps[current_name]['execution_times'] = list(map(float, line.split(':')[1].split()))
        elif 'Polling Point Times:' in line:
                parsing_pp_timestamps = True
                continue
        elif parsing_pp_timestamps and line.strip() and not 'PP Intervals:' in line:
            pp_timestamps.extend(map(float, line.split()))
        elif parsing_pp_timestamps and 'PP Intervals:' in line:
            break


    return timestamps, pp_timestamps


# 读取文件并解析周期和优先级数据
def read_timers_and_callbacks_info(file_path):
    timers_and_callbacks_info = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # 遍历文件的每一行，寻找周期和优先级信息
    for line in lines:
        line = line.strip()
        if line.startswith('Timer') or line.startswith('Sub'):
            parts = line.split(':')
            name = parts[0].strip()
            period_priority = parts[1].strip().split(',')
            period = int(period_priority[0].split('=')[1].strip())
            priority = int(period_priority[1].split('=')[1].strip())
            timers_and_callbacks_info[name] = {'period': period, 'priority': priority}

    return timers_and_callbacks_info

# 绘制图表
def plot_data(timestamps, pp_timestamps, timers_and_callbacks_info):
    fig, ax = plt.subplots(figsize=(12, 8))

    # 为每个对象分配颜色
    colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black']
    color_index = 0

    # 绘制每个 Timer 和 Callback 的执行时间
    for name, data in timestamps.items():
        if data['read_times'] and data['execution_times']:
            for start, exec_time in zip(data['read_times'], data['execution_times']):
                ax.broken_barh([(start, exec_time)], (color_index, 0.8), facecolors=colors[color_index % len(colors)])
            color_index += 1

    # 在每个 Polling Point 画一条竖线，并标注
    # for pp_time in pp_timestamps:
        # ax.axvline(x=pp_time, color='gray', linestyle='--', linewidth=0.5, label='PP' if pp_time == pp_timestamps[0] else "")
    for pp_time in pp_timestamps:
        ax.axvline(x=pp_time, color='orange', linestyle='--', linewidth=0.5)  # 画竖线

    # 设置图表的标题和标签
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Operations')
    ax.set_title('Execution Timeline by Task')

    # 自定义纵轴刻度标签
    ax.set_yticks(range(len(timestamps)))
    ax.set_yticklabels(timestamps.keys())

    # 显示背景的格线，增加网格线的密集度
    ax.grid(True, which='both', linestyle='-', linewidth='0.5', alpha=0.7)
    ax.xaxis.set_major_locator(plt.MultipleLocator(1))
    # 设置横纵轴的范围
    max_time = max(max(data['read_times'], default=0) for data in timestamps.values()) + max(max(data['execution_times'], default=0) for data in timestamps.values())
    if pp_timestamps:
        max_time = max(max_time, max(pp_timestamps))
    ax.set_xlim(0, max_time)
    ax.set_ylim(0, len(timestamps))
    ax.tick_params(axis='x', labelsize='small')  # 设置横轴刻度标签的字体大小

    # 在图表下方添加注释来显示每个 Timer 和 Callback 的信息
    info_text = ""
    for name, info in timers_and_callbacks_info.items():
        info_text += f"{name}: T={info['period']}, P={info['priority']}\n"
    ax.text(0, -0.5, info_text, va='top', ha='left', color='black', fontsize=8)

    # 显示图表
    plt.tight_layout()
    plt.show()

# 主函数
def main():
    file_path = sys.argv[1]
    timestamps, pp_timestamps = read_data(file_path)
    timers_and_callbacks_info = read_timers_and_callbacks_info(file_path)
    plot_data(timestamps, pp_timestamps, timers_and_callbacks_info)


if __name__ == '__main__':
    main()