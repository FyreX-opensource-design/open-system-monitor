import psutil, os, wmi, platform
from util import systemUtil
#import systemUtil

c = wmi.WMI()
wmi_client = wmi.WMI(namespace="root\\cimv2")


def CPUcoreLoad():
    if platform.system() == "Linux" or systemUtil.getWindowsVersion() == 10:
        cpuCores = psutil.cpu_count(logical=False)
        load = psutil.getloadavg()[0]
        return load / cpuCores * 100
    elif systemUtil.getWindowsVersion() == 11:
        return get_cpu_perf_load()

def CPUThreadLoad():
    if platform.system() == "Linux" or systemUtil.getWindowsVersion() == 10:
        threadPercent = psutil.cpu_percent(interval=0.1, percpu=True)
        loadPercent = 0
        for i in threadPercent:
            loadPercent += i
        return round((loadPercent / (len(threadPercent) * 100)) * 100, 2)
    elif systemUtil.getWindowsVersion() == 11:
        cpus = wmi_client.Win32_PerfFormattedData_PerfOS_Processor()
        cpu_loads = []
        for cpu in cpus:
            cpu_loads.append(cpu.PercentProcessorTime)
        loadTotal = 0
        for load in cpu_loads:
            loadTotal += load
        return round((loadTotal / (len(cpu_loads) * 100)) * 100, 2)
#untested, may need some work
def DualCPUload():
    if platform.system() == "Linux" or systemUtil.getWindowsVersion() == 10:
        threadPercent = psutil.cpu_percent(interval=0.1, percpu=True)
        loadA = threadPercent[0:len(threadPercent)/2]
        loadB = threadPercent[len(threadPercent)/2]
        totalA = 0
        totalB = 0
        for i in loadA:
            totalA += i
        for i in loadB:
            totalB += i
        return (round((totalA / (len(loadA) * 100)) * 100, 1),round((totalB / (len(loadB) * 100)) * 100, 1))
    elif systemUtil.getWindowsVersion() == 11:
        cpus = wmi_client.Win32_PerfFormattedData_PerfOS_Processor()
        cpu_loads = []
        for cpu in cpus:
            cpu_loads.append(cpu.PercentProcessorTime)
        loadTotal = 0
        loadA = cpu_loads[0:cpus/2]
        loadB = cpu_loads[cpus/2]
        for i in loadA:
            totalA += i
        for i in loadB:
            totalB += i
        return (round((totalA / (len(loadA) * 100)) * 100, 1),round((totalB / (len(loadB) * 100)) * 100, 1))
    
def get_cpu_perf_load():
    processors = wmi_client.Win32_PerfFormattedData_PerfOS_Processor()
    total_load = 0
    processor_count = 0

    for processor in processors:
        if processor.Name != "_Total":  # Skip total load
            total_load += int(processor.PercentProcessorTime)
            processor_count += 1

    return total_load / processor_count if processor_count > 0 else None