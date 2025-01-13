import wmi

c = wmi.WMI()
#it's advisable to use this to return Windows version, as some psutil functions are inaccurate or don't work on Windows 11
def getWindowsVersion():
    return int(f"{c.Win32_OperatingSystem().os.Name}"[18:20])