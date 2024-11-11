import matplotlib.pyplot as plt
import os
import random

import numpy as np
from scipy import stats
from scipy.signal import periodogram

import re
import sys
from datetime import datetime

class Plot:
    def __init__(self, all_objects):
        self.all_objects = all_objects
        self.name_to_object = {obj.name: obj for obj in self.all_objects}
        self.timestamps = {obj.name: [] for obj in self.all_objects}
        
    def plot(self, filename):
        global runtime
        # 为每个对象分配颜色
        colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black']
        color_map = {obj.name: colors[i % len(colors)] for i, obj in enumerate(all_objects)}

        # 绘制图表
        fig, ax = plt.subplots(figsize=(12, 8))
        fig.subplots_adjust(bottom=0.2)  # 调整底部空间


        # 绘制每个 Timer 和 Callback 的执行时间
        for i, obj in enumerate(all_objects):
            if obj.read_times and obj.execution_times:
                for start, exec_time in zip(obj.read_times, obj.execution_times):
                    ax.broken_barh([(start, exec_time)], (i, 0.8), facecolors=colors[i])

        # 在每个 Polling Point 画一条竖线，并标注
        for pp_time in executor.polling_points:
            ax.axvline(x=pp_time, color='orange', linestyle='--', linewidth=0.5)  # 画竖线

        # 设置图表的标题和标签
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Operations')
        ax.set_title('Execution Timeline by Task')

        # 自定义纵轴刻度标签
        ax.set_yticks(range(len(all_objects)))
        ax.set_yticklabels([obj.name for obj in all_objects])

        # 显示背景的格线，增加网格线的密集度
        ax.grid(True, which='both', linestyle='-', linewidth='0.5', alpha=0.7)
        # ax.xaxis.set_major_locator(plt.MultipleLocator(1))  # 设置x轴主刻度间隔为5秒

        # min_period = min(timer.period for timer in executor.timers)
        # 设置x轴的刻度为最小周期的倍数，这里我们以最小周期为1个单位
        # ax.set_xticks([i * min_period for i in range(1, runtime // min_period + 1)])
        # 设置x轴的刻度标签为最小周期的倍数
        # ax.set_xticklabels([str(i * min_period) for i in range(1, runtime // min_period + 1)])

        ax.xaxis.set_major_locator(plt.MultipleLocator(1))


        # 设置横纵轴的范围
        ax.set_xlim(0, runtime)
        ax.set_ylim(0, len(all_objects))

        # 设置横轴刻度标签的显示格式和字体大小
        ax.tick_params(axis='x', labelsize='small')  # 设置横轴刻度标签的字体大小

        # 在图表下方添加注释来显示每个 Timer 和 Callback 的信息
        info_text = ""
        for obj in executor.timers:
            info_text += f"{obj.name}: T={obj.period}, P={obj.priority}\n"
        for obj in executor.callbacks:
            info_text += f"{obj.name}: P={obj.priority}\n"
        ax.text(0, -0.5, info_text, va='top', ha='left', color='black', fontsize=8)

        # 保存图片
        plt.savefig(filename, dpi=300, bbox_inches='tight')  # PNG格式

        # 显示图表
        plt.show()

class Log:
    def __init__(self, all_objects):
        self.all_objects = all_objects
        self.name_to_object = {obj.name: obj for obj in self.all_objects}
        self.timestamps = {obj.name: [] for obj in self.all_objects}
        
    def output(self, filename):
        # 写入文件
        with open(filename, 'w') as file:
            file.write("#### info ####\n")
            for obj in executor.timers:
                triggered_event = '' 
                if obj.subcallback is not None: 
                    triggered_event = f"{obj.subcallback.name}" 
                else:
                    triggered_event = 'None'
                file.write(f"{obj.name}: T={obj.period:2}, P={obj.priority:2}, Triggered Event={triggered_event}\n")
                # file.write(f"{obj.name}: T={obj.period:2}, P={obj.priority:2}\n")
            for obj in executor.callbacks:
                triggered_event = '' 
                if obj.subcallback is not None: 
                    triggered_event = f"{obj.subcallback.name}" 
                else:
                    triggered_event = 'None'
                file.write(f"{obj.name}: T={obj.period:2}, P={obj.priority:2}, Triggered Event={triggered_event}\n")
                # file.write(f"{obj.name}: T={obj.period:2}, P={obj.priority:2}\n")
            file.write("\n#### read & write & execution time####\n")
            for obj in all_objects:
                file.write(f"\n### {obj.name} ###\n")
                jitter = max(abs(pattern) for pattern in obj.patterns) if obj.patterns else 0
                file.write(f"jitter = {round(jitter,2)}\n")        
                pattern_str = " ".join(f"{t:5.1f}" for t in obj.patterns)
                file.write(f"pattern        : {pattern_str}\n")
                read_times_str = " ".join(f"{t:5.1f}" for t in obj.read_times)
                file.write(f"read       time: {read_times_str}\n")
                write_times_str = " ".join(f"{t:5.1f}" for t in obj.write_times)
                file.write(f"write      time: {write_times_str}\n")
                execution_times_str = " ".join(f"{t:5.1f}" for t in obj.execution_times)
                file.write(f"Execution times: {execution_times_str}\n")



                read_intervals = Statistics.calculate_intervals(obj.read_times)
                write_intervals = Statistics.calculate_intervals(obj.write_times)
                read_intervals_str = " ".join(f"{i:5.1f}" for i in read_intervals)
                file.write(f"Read  Intervals: {read_intervals_str}\n")
                write_intervals_str = " ".join(f"{i:5.1f}" for i in write_intervals)
                file.write(f"Write Intervals: {write_intervals_str}\n")
                read_avg_var_str = f"read  intervals: AVG = {Statistics.calculate_average(read_intervals):.3f}, VAR = {Statistics.calculate_variance(read_intervals):.3f}"
                file.write(f"{read_avg_var_str}\n")
                write_avg_var_str = f"write intervals: AVG = {Statistics.calculate_average(write_intervals):.3f}, VAR = {Statistics.calculate_variance(write_intervals):.3f}"
                file.write(f"{write_avg_var_str}\n")

            pp_times_str = " ".join(f"{t:.1f}" for t in executor.polling_points)
            file.write(f"\nPolling Point: {pp_times_str}\n")
            pp_intervals = Statistics.calculate_intervals(executor.polling_points)
            pp_intervals_str = " ".join(f"{i:.1f}" for i in pp_intervals)
            file.write(f"PP  Intervals: {pp_intervals_str}\n")
            pp_avg_var_str = f"AVG = {Statistics.calculate_average(pp_intervals):.2f}, VAR = {Statistics.calculate_variance(pp_intervals):.2f}"
            file.write(f"{pp_avg_var_str}\n")


            # 在写入文件之后，画图之前调用 check_read_time_between_others 函数
            parallel_results = Statistics.check_read_time_between_others(all_objects)

            # 打印结果
            if parallel_results:
                print("Detected read times between other objects' read and write times:")
                file.write("\nDetected read times between other objects' read and write times:\n")
                for result in parallel_results:
                    file.write(f"Object {result[0]} at time {result[2]}s is between {result[1]}'s read and write times ({result[3]})\n")
                    print(f"Object {result[0]} at time {result[2]}s is between {result[1]}'s read and write times ({result[3]})")
            else:
                print("No read times detected between other objects' read and write times.")
                file.write("\nNo read times detected between other objects' read and write times.\n")

        
class Statistics:
    @staticmethod
    def calculate_theta_series(instance, all_tasks):
        """计算特定实例的一系列理论theta值"""
        theta_series = []
        max_multiple = max(len(task.execution_times) for task in all_tasks)  # 假设所有任务的执行次数不超过其他任务执行时间列表的长度
        for j in range(1, max_multiple + 1):  # 遍历所有Ti的整数倍
            theta = 0
            for task_h in all_tasks:
                if task_h.priority > instance.priority:  # 只考虑优先级高于当前实例的任务
                    n = j * instance.period // task_h.period  # 计算n使得jTi = nTh
                    if n * task_h.period == j * instance.period:  # 检查是否精确相等
                        if len(task_h.execution_times) >= n:  # 确保有足够的执行时间
                            theta += task_h.execution_times[n - 1]  # 累加第n个执行时间
            theta_series.append(theta)
        return theta_series
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

    def check_read_time_between_others(all_objects):
    # 存储检测结果
        results = []

        # 遍历所有对象
        for i, obj1 in enumerate(all_objects):
            # 遍历所有其他对象
            for j, obj2 in enumerate(all_objects):
                if i != j:  # 避免自身比较
                    # 检查 obj1 的每个读时间是否在 obj2 的读时间和写时间之间
                    for read_time1 in obj1.read_times:
                        if any(obj2.read_times[i] < read_time1 < obj2.write_times[i] for i in range(len(obj2.read_times))):
                            results.append((obj1.name, obj2.name, read_time1, "between read and write times"))

                    # 检查 obj1 的每个写时间是否在 obj2 的读时间和写时间之间
                    for write_time1 in obj1.write_times:
                        if any(obj2.read_times[i] < write_time1 < obj2.write_times[i] for i in range(len(obj2.read_times))):
                            results.append((obj1.name, obj2.name, write_time1, "between read and write times"))

        return results


class Timer:
    def __init__(self, name, period, priority):
        self.name = name
        self.period = period
        self.priority = priority
        self.next_execution_time = 0  # 初始时间为周期后
        self.subcallback = None
        self.buffer = None  # 为定时器创建一个buffer，大小为1
        self.read_times = []
        self.write_times = []
        self.execution_times = []  # 用于存储每次执行的时间
        self.index = 1
        self.patterns = []
        

    def execute(self):
        global current_time
        if self.subcallback:
            self.subcallback.period = self.period
        self.read_times.append(current_time)
        
        pattern = current_time - (self.index - 1) * self.period
        self.patterns.append(pattern)

        # execution_time = round(random.uniform(0.1, 0.5), 1)  # 每次执行时随机生成执行时间
        execution_time = 0.8

        current_time += execution_time
        current_time = round(current_time, 2)
        self.write_times.append(current_time)
        self.execution_times.append(execution_time)  # 记录执行时间
        self.next_execution_time = self.index * self.period  # 更新下一个执行时间
        self.buffer = self.subcallback  # 更新buffer为最新的回调
        self.index += 1
        

    def is_ready(self, current_time):
        return current_time >= self.next_execution_time

    def __lt__(self, other):
        return self.priority < other.priority
    


class Callback:
    def __init__(self, name, priority, triggers_new):
        self.name = name        
        self.priority = priority
        self.subcallback = None
        self.buffer = None  # 为定时器创建一个buffer，大小为1
        self.triggers_new = triggers_new
        self.read_times = []
        self.write_times = []
        self.execution_times = []  # 用于存储每次执行的时间
        self.index = 1
        self.period = None
        self.patterns = []
        

    def execute(self):
        global current_time
        if self.subcallback:
            self.subcallback.period = self.period
        self.read_times.append(current_time)
        pattern = current_time - (self.index - 1) * self.period
        self.patterns.append(pattern)

        # execution_time = round(random.uniform(0.1, 0.5), 1)  # 每次执行时随机生成执行时间
        execution_time = 0.8

        current_time += execution_time
        current_time = round(current_time, 2)
        self.write_times.append(current_time)
        self.execution_times.append(execution_time)  # 记录执行时间
        if self.triggers_new is True:
            self.buffer = self.subcallback

        self.index += 1

        ready_timers = [t for t in executor.timers if t.is_ready(current_time)]
        if ready_timers:
            ready_timers.sort()  # 按优先级排序
            for t in ready_timers:
                t.next_execution_time += current_time - t.next_execution_time 



    def __lt__(self, other):
        return self.priority < other.priority
    

class Executor:
    def __init__(self):
        self.timers = []
        self.readyset = []
        self.callbacks = []
        self.polling_points = []

    def add_timer(self, timer):
        self.timers.append(timer)
    
    def add_callback(self, callback):
        self.callbacks.append(callback)

    def run(self, runtime):
        global current_time
        global is_executing
        pp = 0
        while current_time < runtime:  # 模拟运行30秒
            # 收集所有已就绪的定时器
            ready_timers = [t for t in self.timers if t.is_ready(current_time)]
            ready_timers.sort()  # 按优先级排序

            if not is_executing:
                while ready_timers:
                    timer = ready_timers.pop(0)  # 执行优先级最高的定时器
                    is_executing = True
                    timer.execute()
                    is_executing = False
                    # 再次检查是否有新的定时器就绪
                    ready_timers = [t for t in self.timers if t.is_ready(current_time)]
                    ready_timers.sort()  # 重新排序

            # 检查readyset是否为空
            if not ready_timers and self.readyset and not is_executing:
                # 如果没有就绪的定时器并且readyset不空，执行callback
                ready_callbacks = sorted(self.readyset, key=lambda x: x.priority)
                # for callback in ready_callbacks:
                callback = ready_callbacks[0]
                self.readyset.remove(callback)
                is_executing = True
                callback.execute()
                is_executing = False
            
            # 如果没有就绪的定时器和readyset为空，更新轮询点
            if not ready_timers and not self.readyset and not is_executing:
                # 更新轮询点时间                
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
                if self.readyset:
                    pp += 1
                    self.polling_points.append(current_time)
                else:
                    current_time = self.get_next_timer_time()
                    current_time = round(current_time, 2)
                
    def get_next_timer_time(self):
        # 找到下一个就绪的定时器时间
        next_times = [t.next_execution_time for t in self.timers]
        if next_times:
            return min(next_times)

                

# 全局变量，用于跟踪当前时间
global current_time
current_time = 0
global is_executing
is_executing = False

output_file_base = sys.argv[1] if len(sys.argv) > 1 else "output"
runtime = float(sys.argv[2]) if len(sys.argv) > 2 else 120

# 获取当前时间并格式化为字符串
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# 在输出文件名后面加入时间戳
output_file_name = f"{output_file_base}_{timestamp}"

file_path = f'result/{output_file_name}.txt'
plot_path = f'result/{output_file_name}.png'

# 创建执行器实例
executor = Executor()

timer1 = Timer("Timer1", 3, 1)
timer2 = Timer("Timer2", 4, 2)
timer3 = Timer("Timer3", 5, 3)

callback1 = Callback("Sub1", 4, triggers_new=False)
callback2 = Callback("Sub2", 5, triggers_new=False)
callback3 = Callback("Sub3", 6, triggers_new=True)
callback4 = Callback("Sub4", 7, triggers_new=False)

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

# analysis
# 从 Executor 实例中获取 Timer 和 Callback 列表
all_objects = executor.timers + executor.callbacks
# all_objects = [timer1, timer2, callback1, callback2, timer3, callback3, callback4]

Log.output(all_objects, file_path)
Plot.plot(all_objects, plot_path)

