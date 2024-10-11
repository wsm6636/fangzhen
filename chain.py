import matplotlib.pyplot as plt
import os
import random
import networkx as nx

class OutputManager:
    def __init__(self, filename):
        self.filename = filename
        self.events = []  # 用于存储输出事件
        if os.path.exists(self.filename):
            # 如果文件存在，删除它
            os.remove(self.filename)
    def write(self, message):
        with open(self.filename, 'a') as file:
            file.write(message + '\n')
        print(message)  # 同时打印到屏幕
        self.events.append(message)  # 将事件添加到列表中

class Timer:
    def __init__(self, name, period, priority, output_manager):
        self.name = name
        self.execution_time = round(random.uniform(0.1, 0.5), 1)
        self.period = period
        self.priority = priority
        self.next_execution_time = 0  # 初始时间为周期后
        self.subcallback = None
        self.buffer = None  # 为定时器创建一个buffer，大小为1
        self.output_manager = output_manager
        self.read_times = []
        self.write_times = []
        print(f"Created Timer '{self.name}' with period {self.period}, priority {self.priority}, and execution time {self.execution_time}")  # 打印信息

    def execute(self):
        global current_time
        self.read_times.append(current_time)
        self.output_manager.write(f"{self.name} at {current_time}s")
        # print(f"Timer {self.name} executed at {current_time}s")
        current_time += self.execution_time
        current_time = round(current_time, 2)
        self.next_execution_time += self.period  # 更新下一个执行时间
        self.buffer = self.subcallback  # 更新buffer为最新的回调
        self.write_times.append(current_time)

    def is_ready(self, current_time):
        return current_time >= self.next_execution_time

    def __lt__(self, other):
        return self.priority < other.priority

class Callback:
    def __init__(self, name, priority, output_manager, triggers_new):
        self.name = name
        self.execution_time = round(random.uniform(0.1, 0.5), 1)
        self.priority = priority
        self.subcallback = None
        self.buffer = None  # 为定时器创建一个buffer，大小为1
        self.triggers_new = triggers_new
        self.output_manager = output_manager
        print(f"Created Callback '{self.name}' with priority {self.priority}, and execution time {self.execution_time}")  # 打印信息
        self.read_times = []
        self.write_times = []
        

    def execute(self):
        global current_time
        self.read_times.append(current_time)
        self.output_manager.write(f"{self.name} at {current_time}s")
        # print(f"Callback {self.name} executed at {current_time}s")
        current_time += self.execution_time
        current_time = round(current_time, 2)
        if self.triggers_new is True:
            self.buffer = self.subcallback
        self.write_times.append(current_time)

    def __lt__(self, other):
        return self.priority < other.priority

class Executor:
    def __init__(self, output_manager):
        self.timers = []
        self.readyset = []
        self.callbacks = []
        self.output_manager = output_manager

    def add_timer(self, timer):
        self.timers.append(timer)
        print()
    
    def add_callback(self, callback):
        self.callbacks.append(callback)

    def run(self, runtime):
        global current_time
        # current_time = 0
        pp = 0
        while current_time < runtime:  # 模拟运行30秒
            # 收集所有已就绪的定时器
            ready_timers = [t for t in self.timers if t.is_ready(current_time)]
            ready_timers.sort()  # 按优先级排序

            while ready_timers:
                timer = ready_timers.pop(0)  # 执行优先级最高的定时器
                timer.execute()
                # 再次检查是否有新的定时器就绪
                ready_timers = [t for t in self.timers if t.is_ready(current_time)]
                ready_timers.sort()  # 重新排序

            # 检查readyset是否为空
            if not ready_timers and self.readyset:
                # 如果没有就绪的定时器并且readyset不空，执行callback
                ready_callbacks = sorted(self.readyset, key=lambda x: x.priority)
                # for callback in ready_callbacks:
                callback = ready_callbacks[0]
                self.readyset.remove(callback)
                callback.execute()

            # 如果没有就绪的定时器和readyset为空，更新轮询点
            if not ready_timers and not self.readyset:
                # 更新轮询点时间
                pp += 1
                self.output_manager.write(f"Polling point {pp} at {current_time}s")
                # print(f"Polling point {pp} at {current_time}s")
                # 将所有定时器的buffer中的回调放入readyset，并清空buffer
                for timer in self.timers:
                    if timer.buffer:
                        self.readyset.append(timer.buffer)
                        timer.buffer = None  # 清空buffer
                for callback in self.callbacks:
                    if callback.buffer:
                        self.readyset.append(callback.buffer)
                        callback.buffer = None
                if not self.readyset:
                    current_time = self.get_next_timer_time()
                    current_time = round(current_time, 2)
                    
    def get_next_timer_time(self):
        # 找到下一个就绪的定时器时间
        next_times = [t.next_execution_time for t in self.timers]
        if next_times:
            return min(next_times)
        # else:
            # return current_time  # 如果没有更多的定时器，保持当前时间
class Statistics:
    #平均值
    @staticmethod
    def calculate_average(values):
        avg = sum(values) / len(values) if values else 0
        return round(avg, 3)
    #方差
    @staticmethod
    def calculate_variance(values):
        var = sum((x - (sum(values) / len(values))) ** 2 for x in values) / len(values) if values else 0        
        return round(var, 3)
    #差值
    @staticmethod
    def calculate_time_difference(start_time, end_time):
        return end_time - start_time
    #相邻任务对间隔
    @staticmethod
    def calculate_intervals(times):
        """
        计算时间列表中前后两两元素的间隔。
        :param times: 时间列表。
        :return: 时间间隔列表。
        """
        return [Statistics.calculate_time_difference(times[i], times[i+1]) for i in range(len(times) - 1)]
    @staticmethod
    def calculate_timer_theory_time(timers):
        """
        计算Timer的理论时间。
        :param timers: Timer对象列表。
        :return: 理论时间列表。
        """
        timer_theory_times = []
        for timer in timers:
            # 假设Timer连续触发，计算理论触发时间点
            theory_time = 0
            while theory_time <= Statistics.calculate_average([timer.period for timer in timers]):
                timer_theory_times.append(theory_time)
                theory_time += timer.period
        return timer_theory_times

    @staticmethod
    def calculate_callback_theory_time(callbacks, timers):
        """
        计算Callback的理论时间。
        :param callbacks: Callback对象列表。
        :param timers: Timer对象列表，用于获取触发此Callback的任务的优先级。
        :return: 理论时间列表。
        """
        callback_theory_times = []
        for callback in callbacks:
            # 获取触发此Callback的任务的Timer
            triggering_timer = next((timer for timer in timers if timer.subcallback == callback), None)
            if triggering_timer:
                # 假设Callback在触发它的Timer的理论时间点之后立即执行
                theory_time = 0
                while theory_time <= Statistics.calculate_average([triggering_timer.period for timer in timers if timer.subcallback == callback]):
                    callback_theory_times.append(theory_time)
                    theory_time += triggering_timer.period + callback.execution_time
        return callback_theory_times

# 全局变量，用于跟踪当前时间
global current_time
current_time = 0

runtime = 60

output_manager = OutputManager('output.txt')

# 创建执行器实例
executor = Executor(output_manager)

timer1 = Timer("Timer1", 3, 1, output_manager)
timer2 = Timer("Timer2", 4, 2, output_manager)
timer3 = Timer("Timer3", 5, 3, output_manager)

callback1 = Callback("Sub1", 4, output_manager, triggers_new=False)
callback2 = Callback("Sub2", 5, output_manager, triggers_new=False)
callback3 = Callback("Sub3", 6, output_manager, triggers_new=True)
callback4 = Callback("Sub4", 7, output_manager, triggers_new=False)

timer1.subcallback = callback1
timer2.subcallback = callback2
timer3.subcallback = callback3

callback3.subcallback = callback4

# 创建并添加定时器
executor.add_timer(timer1)
executor.add_timer(timer2)
executor.add_timer(timer3)


executor.add_callback(callback1)
executor.add_callback(callback2)
executor.add_callback(callback3)
executor.add_callback(callback4)

# 运行执行器
executor.run(runtime)

# 从 Executor 实例中获取 Timer 和 Callback 列表
all_objects = executor.timers + executor.callbacks

# 创建一个映射，将 Timer 和 Callback 的名称映射到它们的对象实例
name_to_object = {obj.name: obj for obj in all_objects}

# 为每个对象分配颜色
colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black']
color_map = {obj.name: colors[i % len(colors)] for i, obj in enumerate(all_objects)}

# 解析事件并记录每个 Timer 和 Callback 的执行时间点
timestamps = {obj.name: [] for obj in all_objects}
pp_timestamps = []  # 提取 Polling Points 的时间

with open('output.txt', 'r') as file:
    for line in file:
        parts = line.split(" at ")
        if len(parts) > 1:
            label = parts[0].strip()
            timestamp = float(parts[1].split("s")[0])
            if label in name_to_object:
                timestamps[label].append(timestamp)
            elif "Polling point" in line:
                pp_timestamps.append(timestamp)


# 按优先级排序
all_objects.sort()
# for timer in timers:
#     read_intervals = Statistics.calculate_intervals(timer.read_times)
#     write_intervals = Statistics.calculate_intervals(timer.write_times)
#     print(f"Timer {timer.name} Read Intervals: {read_intervals}")
#     print(f"Timer {timer.name} Write Intervals: {write_intervals}")

# for callback in callbacks:
#     read_intervals = Statistics.calculate_intervals(callback.read_times)
#     write_intervals = Statistics.calculate_intervals(callback.write_times)
#     print(f"Callback {callback.name} Read Intervals: {read_intervals}")
#     print(f"Callback {callback.name} Write Intervals: {write_intervals}")

# 写入文件
with open('read_write_times.txt', 'w') as file:
    file.write(f"### info ###\n")
    for obj in executor.timers:
        file.write(f"{obj.name}: T={obj.period}, P={obj.priority}, E={obj.execution_time} \n")
    for obj in executor.callbacks:
        file.write(f"{obj.name}: P={obj.priority}, E={obj.execution_time}\n")
    file.write(f"\n### read & write time ###\n")
    for obj in all_objects:
        file.write(f"\n### {obj.name} ###\n")
        file.write("read  time: " + " ".join(f"{t:.1f}" for t in obj.read_times) + "\n")
        file.write("write time: " + " ".join(f"{t:.1f}" for t in obj.write_times) + "\n")

        file.write(f"\nread  time: AVG = {Statistics.calculate_average(obj.read_times)}, VAR = {Statistics.calculate_variance(obj.read_times)}\n")
        file.write(f"write time: AVG = {Statistics.calculate_average(obj.write_times)}, VAR = {Statistics.calculate_variance(obj.write_times)}\n")
        
        read_intervals = Statistics.calculate_intervals(obj.read_times)
        write_intervals = Statistics.calculate_intervals(obj.write_times)
        file.write("\nRead  Intervals: ")
        file.write(" ".join(f"{i:.1f}" for i in read_intervals) + "\n")
        
        file.write("Write Intervals: ")
        file.write(" ".join(f"{i:.1f}" for i in write_intervals) + "\n")



# 绘制图表
fig, ax = plt.subplots(figsize=(12, 8))
fig.subplots_adjust(bottom=0.2)  # 调整底部空间

# 绘制每个 Timer 和 Callback 的执行时间
y_positions = {obj.name: i for i, obj in enumerate(all_objects)}
for label, times in timestamps.items():
    if times:
        execution_time = name_to_object[label].execution_time
        for timestamp in times:
            ax.broken_barh([(timestamp, execution_time)], (y_positions[label], 0.5), facecolors=color_map[label])

# 在每个 Polling Point 画一条竖线，并标注
for pp_time in pp_timestamps:
    ax.axvline(x=pp_time, color='grey', linestyle='--', linewidth=0.5)  # 画竖线

# 设置图表的标题和标签
ax.set_xlabel('Time (s)')
ax.set_ylabel('Operations')
ax.set_title('Execution Timeline by Task')

# 自定义纵轴刻度标签
ax.set_yticks(range(len(all_objects)))
ax.set_yticklabels(list(y_positions.keys()))

# 显示背景的格线，增加网格线的密集度
ax.grid(True, which='both', linestyle='-', linewidth='0.5', alpha=0.7)
# ax.xaxis.set_major_locator(plt.MultipleLocator(1))  # 设置x轴主刻度间隔为5秒

min_period = min(timer.period for timer in executor.timers)
# 设置x轴的刻度为最小周期的倍数，这里我们以最小周期为1个单位
ax.set_xticks([i * min_period for i in range(1, runtime // min_period + 1)])
# 设置x轴的刻度标签为最小周期的倍数
ax.set_xticklabels([str(i * min_period) for i in range(1, runtime // min_period + 1)])

# 设置横纵轴的范围
ax.set_xlim(0, runtime)
ax.set_ylim(-1, len(all_objects))

# 设置横轴刻度标签的显示格式和字体大小
ax.tick_params(axis='x', labelsize='small')  # 设置横轴刻度标签的字体大小

# 在图表下方添加注释来显示每个 Timer 和 Callback 的信息
info_text = ""
for obj in executor.timers:
    info_text += f"{obj.name}: T={obj.period}, P={obj.priority}, E={obj.execution_time}, AVG = {Statistics.calculate_average(obj.read_times)}, VAR = {Statistics.calculate_variance(obj.read_times)}\n"
for obj in executor.callbacks:
    info_text += f"{obj.name}: P={obj.priority}, E={obj.execution_time}, AVG = {Statistics.calculate_average(obj.read_times)}, VAR = {Statistics.calculate_variance(obj.read_times)}\n"
ax.text(0, -1.5, info_text, va='top', ha='left', color='black', fontsize=8)



# 保存图片
plt.savefig('output.png')

# 显示图表
plt.show()