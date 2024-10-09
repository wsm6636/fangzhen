class Timer:
    def __init__(self, name, period, execution_time, priority):
        self.name = name
        self.period = period
        self.execution_time = execution_time
        self.priority = priority
        self.next_execution_time = 0  # 初始时间为周期后
        self.subcallback = None
        self.buffer = None  # 为定时器创建一个buffer，大小为1

    def execute(self):
        global current_time
        print(f"Timer {self.name} executed at {current_time}s")
        current_time += self.execution_time
        self.next_execution_time += self.period  # 更新下一个执行时间
        self.buffer = self.subcallback  # 更新buffer为最新的回调

    def is_ready(self, current_time):
        return current_time >= self.next_execution_time

    def __lt__(self, other):
        return self.priority < other.priority

class Callback:
    def __init__(self, name, execution_time, priority, triggers_new):
        self.name = name
        self.execution_time = execution_time
        self.priority = priority
        self.subcallback = None
        self.buffer = None  # 为定时器创建一个buffer，大小为1
        self.triggers_new = triggers_new

    def execute(self):
        global current_time
        print(f"Callback {self.name} executed at {current_time}s")
        current_time += self.execution_time
        if self.triggers_new is True:
            self.buffer = self.subcallback

    def __lt__(self, other):
        return self.priority < other.priority

class Executor:
    def __init__(self):
        self.timers = []
        self.readyset = []
        self.callbacks = []

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
                print(f"Polling point {pp} at {current_time}s")
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

# 创建执行器实例
executor = Executor()

timer1 = Timer("Timer1", 5, 1, 1)
timer2 = Timer("Timer2", 5, 1, 2)
timer3 = Timer("Timer3", 10, 1, 3)

callback1 = Callback("Sub1", 1, 4, triggers_new=False)
callback2 = Callback("Sub2", 1, 5, triggers_new=False)
callback3 = Callback("Sub3", 1, 6, triggers_new=True)
callback4 = Callback("Sub4", 1, 7, triggers_new=False)

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