import psutil, os, subprocess, platform
from util import systemUtil
#import systemUtil

def getCpuloadLinux():
    if platform.system() == "Linux":
        threadPercent = psutil.cpu_percent(interval=0.1, percpu=True)
        loadPercent = 0
        for i in threadPercent:
            loadPercent += i
        return round(loadPercent / len(threadPercent), 2)
    else:
        return "command is Linux only"
    
def getCpuLoadWindows():
    if platform.system() != "Linux":
        try:
            # Run the typeperf command to fetch CPU load
            process = subprocess.run(
                ["typeperf", "\\Processor(_Total)\\% Processor Time", "-sc", "1"],
                text=True,
                capture_output=True,
                check=True
            )
            # Extract CPU load from the output
            lines = process.stdout.splitlines()
            if len(lines) > 2:
                # Parse the value from the second last line
                cpu_load = lines[2].split(",")[-1].strip().replace('"', '')
                return round(float(f"{cpu_load}"), 1) 
        except Exception as e:
            return f"Failed to get CPU load: {e}"
    else:
        return "command is Windows only"