import matplotlib.pyplot as plt

class OutputManager:
    def __init__(self, filename):
        self.filename = filename
        self.events = []  # 用于存储输出事件

    def write(self, message):
        with open(self.filename, 'a') as file:
            file.write(message + '\n')
        print(message)  # 同时打印到屏幕
        self.events.append(message)  # 将事件添加到列表中

class Timer:
    def __init__(self, name, period, execution_time, priority, output_manager):
        self.name = name
        self.period = period
        self.execution_time = execution_time
        self.priority = priority
        self.next_execution_time = 0  # 初始时间为周期后
        self.subcallback = None
        self.buffer = None  # 为定时器创建一个buffer，大小为1
        self.output_manager = output_manager

    def execute(self):
        global current_time
        self.output_manager.write(f"{self.name} at {current_time}s")
        # print(f"Timer {self.name} executed at {current_time}s")
        current_time += self.execution_time
        self.next_execution_time += self.period  # 更新下一个执行时间
        self.buffer = self.subcallback  # 更新buffer为最新的回调

    def is_ready(self, current_time):
        return current_time >= self.next_execution_time

    def __lt__(self, other):
        return self.priority < other.priority

class Callback:
    def __init__(self, name, execution_time, priority, output_manager, triggers_new):
        self.name = name
        self.execution_time = execution_time
        self.priority = priority
        self.subcallback = None
        self.buffer = None  # 为定时器创建一个buffer，大小为1
        self.triggers_new = triggers_new
        self.output_manager = output_manager

    def execute(self):
        global current_time
        self.output_manager.write(f"{self.name} at {current_time}s")
        # print(f"Callback {self.name} executed at {current_time}s")
        current_time += self.execution_time
        if self.triggers_new is True:
            self.buffer = self.subcallback

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


# 全局变量，用于跟踪当前时间
global current_time
current_time = 0

runtime = 60

output_manager = OutputManager('output.txt')

# 创建执行器实例
executor = Executor(output_manager)

timer1 = Timer("Timer1", 5, 1, 1, output_manager)
timer2 = Timer("Timer2", 5, 1, 2, output_manager)
timer3 = Timer("Timer3", 10, 1, 3, output_manager)

callback1 = Callback("Sub1", 1, 4, output_manager, triggers_new=False)
callback2 = Callback("Sub2", 1, 5, output_manager, triggers_new=False)
callback3 = Callback("Sub3", 1, 6, output_manager, triggers_new=True)
callback4 = Callback("Sub4", 1, 7, output_manager, triggers_new=False)

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

# 解析输出事件
events = []
with open('output.txt', 'r') as file:
    events = file.readlines()

# 创建一个映射，将Timer和Callback的名称映射到它们的对象实例
name_to_object = {}
name_to_object[timer1.name] = timer1
name_to_object[timer2.name] = timer2
name_to_object[timer3.name] = timer3
name_to_object[callback1.name] = callback1
name_to_object[callback2.name] = callback2
name_to_object[callback3.name] = callback3
name_to_object[callback4.name] = callback4

# 提取执行时间和标签
timestamps = {}
for event in events:
    parts = event.split(" at ")
    if len(parts) > 1 and parts[0].strip() in name_to_object:  # 只考虑Timer和Callback的事件
        label = parts[0].strip()
        timestamp = float(parts[1].split("s")[0])
        if label not in timestamps:
            timestamps[label] = []
        timestamps[label].append(timestamp)

# 提取Polling Points
pp_timestamps = [float(event.split(" at ")[1].split("s")[0]) for event in events if "Polling point" in event]

# 为每个Timer和Callback分配颜色
colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black']
color_map = {timer1.name: colors[0], timer2.name: colors[1], timer3.name: colors[2],
             callback1.name: colors[3], callback2.name: colors[4], callback3.name: colors[5], callback4.name: colors[6]}

# 绘制图表
fig, ax = plt.subplots(figsize=(12, 8))  # 调整画布大小

# 绘制每个Timer和Callback的执行时间
y_positions = {}
current_y = 0
label_names = sorted(name_to_object.keys(), key=lambda x: name_to_object[x].priority, reverse=True)
for label in label_names:
    y_positions[label] = current_y
    if label in timestamps:
        execution_time = name_to_object[label].execution_time
        for timestamp in timestamps[label]:
            ax.broken_barh([(timestamp, execution_time)], (y_positions[label], 0.5), facecolors=color_map[label])  # 设置高度为0.5
    current_y += 1


# 在每个Polling Point画一条竖线，并标注
for pp_time in pp_timestamps:
    ax.axvline(x=pp_time, color='grey', linestyle='--', linewidth=1)  # 画竖线
    ax.text(pp_time, current_y + 0.5, '', va='bottom', ha='center', color='grey', fontsize=9)  # 标注PP

# 设置图表的标题和标签
ax.set_xlabel('Time (s)')
ax.set_ylabel('Operations')
ax.set_title('Execution Timeline by Task')

# 自定义纵轴刻度标签
y_ticks = list(y_positions.values())
y_labels = list(y_positions.keys())
ax.set_yticks(y_ticks)
ax.set_yticklabels(y_labels)

# 显示背景的格线，增加网格线的密集度
ax.grid(True, which='both', linestyle='-', linewidth='0.5', alpha=0.7)
ax.xaxis.set_major_locator(plt.MultipleLocator(1))  # 设置x轴主刻度间隔为5秒
ax.yaxis.set_major_locator(plt.MultipleLocator(1))  # 设置y轴主刻度间隔为1

# 设置横纵轴的范围
ax.set_xlim(0, runtime)
ax.set_ylim(0, current_y)

# 设置横轴刻度标签的显示格式
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda val, pos: f'{int(val)}'))
ax.tick_params(axis='x', labelsize='small')  # 设置横轴刻度标签的字体大小

# 保存图片
plt.savefig('output.png')

# 显示图表
plt.show()