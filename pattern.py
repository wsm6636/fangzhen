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
            execution_times = list(map(float, line.split(':')[1].split()))
            timestamps[current_name]['execution_times'] = execution_times

    return timestamps

# 读取文件并解析周期和优先级数据
def read_timers_and_callbacks_info(file_path):
    events_info = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if line.startswith('Timer') or line.startswith('Sub'):
            parts = line.split(':')
            name = parts[0].strip()
            info = parts[1].strip().split(',')
            period = int(info[0].split('=')[1].strip())
            priority = int(info[1].split('=')[1].strip())
            trigger = info[2].split('=')[1].strip()
            events_info[name] = {'period': period, 'priority': priority, 'trigger':trigger}

    return events_info

# 计算theta序列
def calculate_theta(events_info, timestamps):
    sorted_events = sorted(events_info.items(), key=lambda x: x[1]['priority'])
    for name, event_info in sorted_events:
        period = event_info['period']
        thetas = []
        theta = 0
        for n in range(len(timestamps[name]['execution_times'])):
            for other_name, other_info in sorted_events:
                if other_info['priority'] < event_info['priority']:
                    for m in range(len(timestamps[other_name]['execution_times'])):
                        if m * other_info['period'] == n * period:
                            theta += timestamps[other_name]['execution_times'][m]
            theta = round(theta,1)
            thetas.append(theta)

        timestamps[name]['thetas'] = thetas

# 计算jitter序列
def calculate_jitter(events_info, timestamps):
    sorted_events = sorted(events_info.items(), key=lambda x: x[1]['priority'])
    for name, event_info in sorted_events:
        period = event_info['period']
        priority = event_info['priority']
        jitters = []
        jitter = 0
        
        if priority is not 1:
            for n in range(len(timestamps[name]['execution_times'])):
                for other_name, other_info in sorted_events:
                    if other_info['priority'] < event_info['priority']:
                        for m in range(len(timestamps[other_name]['execution_times'])):
                            if timestamps[name]['thetas'][n] == m * period:
                                jitter += timestamps[other_name]['execution_times'][m]
                jitter = round(jitter, 1)
                jitters.append(jitter)
        else:
            

        timestamps[name]['jitters'] = jitters


def calculate_jitter_highest(events_info, timestamps):
    sorted_events = sorted(events_info.items(), key=lambda x: x[1]['priority'])
    for name, event_info in sorted_events:
        period = event_info['period']
        priority = event_info['priority']
        jitters = []
        jitter = 0
        if priority is 1:
        for m in range(len(timestamps[other_name]['execution_times'])):
            block = m * other_info['period'] + timestamps[other_name]['thetas'][m] + timestamps[other_name]['jitters'][m] 
            block_exec = m * other_info['period'] + timestamps[other_name]['thetas'][m] + timestamps[other_name]['jitters'][m] + timestamps[other_name]['execution_times'][m]
            if block < n * period and n * period < block_exec:
                jitter = block_exec - n * period

# 计算pattern序列
def calculate_pattern(timestamps):
    patterns = {}

    for name, info in timestamps.items():
        thetas = info.get('thetas', [])
        jitters = info.get('jitters', [])
        patterns[name] = [round((theta + jitter),1) for theta, jitter in zip(thetas, jitters)]

    return patterns



# 将结果写入文件
def write_results_to_file(patterns, output_filename):
    with open(output_filename, 'w') as output_file:
        for name, pattern in patterns.items():
            output_file.write(f"{name}: pattern={pattern}\n")

# 主程序
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)

    inputfilename = sys.argv[1]
    outputfilename = sys.argv[2]
    events_info = read_timers_and_callbacks_info(inputfilename)
    timestamps = read_data(inputfilename)
    calculate_theta(events_info, timestamps)
    calculate_jitter(events_info, timestamps)
    patterns = calculate_pattern(timestamps)
    write_results_to_file(patterns, outputfilename)