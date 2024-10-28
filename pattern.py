import re
import sys

# 读取文件并解析数据
def read_data(file_path):
    timestamps = {}

    with open(file_path, 'r') as file:
        lines = file.readlines()

    current_name = None
    for line in lines:
        line = line.strip()
        if line.startswith('### '):
            current_name = line.split('###')[1].strip()
            timestamps[current_name] = {'execution_times': []}
        elif current_name and 'Execution times:' in line:
            timestamps[current_name]['execution_times'] = list(map(float, line.split(':')[1].split()))

    return timestamps


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
            info = parts[1].strip().split(',')
            period = int(info[0].split('=')[1].strip())
            priority = int(info[1].split('=')[1].strip())
            trigger = info[2].split('=')[1].strip()
            timers_and_callbacks_info[name] = {'period': period, 'priority': priority, 'trigger': trigger}

    return timers_and_callbacks_info



inputfilename = sys.argv[1]
print(read_timers_and_callbacks_info(inputfilename))
print(read_data(inputfilename))