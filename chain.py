import threading
import time

class Timer:
    def __init__(self, name, period, callback):
        self.name = name
        self.period = period
        self.callback = callback
        self.thread = threading.Thread(target=self.run)
        self.shutdown = False

    def run(self):
        while not self.shutdown:
            start_time = time.time()
            self.callback()
            execution_time = time.time() - start_time
            sleep_time = self.period - execution_time
            if sleep_time > 0:
                time.sleep(sleep_time)

    def start(self):
        self.thread.start()

    def stop(self):
        self.shutdown = True
        self.thread.join()

class Subscription:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

    def callback(self):
        print(f"Subscription {self.name} callback executed.")

def main():
    # 创建订阅
    sub1 = Subscription("Sub1", 3)
    sub2 = Subscription("Sub2", 2)
    sub3 = Subscription("Sub3", 1)

    # 创建定时器
    timer1 = Timer("Timer1", 5, sub1.callback)
    timer2 = Timer("Timer2", 7, sub2.callback)
    timer3 = Timer("Timer3", 8, sub3.callback)

    # 根据优先级（周期）对定时器进行排序
    timers = sorted([timer1, timer2, timer3], key=lambda t: t.period)

    # 启动定时器
    for timer in timers:
        timer.start()

    # 运行一段时间后停止定时器
    time.sleep(10)
    timer1.stop()
    timer2.stop()
    timer3.stop()

if __name__ == "__main__":
    main()