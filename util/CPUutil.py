import psutil
# not working under Windows. Seems to be a psutil bug or a change in Windows itself
def CPUcoreLoad():
    cpuCores = psutil.cpu_count(logical=False)
    load = psutil.getloadavg()[0]
    return load / cpuCores * 100

def CPUThreadLoad():
    threadPercent = psutil.cpu_percent(interval=0.1, percpu=True)
    loadPercent = 0
    for i in threadPercent:
        loadPercent += i
    return round((loadPercent / (len(threadPercent) * 100)) * 100, 2)