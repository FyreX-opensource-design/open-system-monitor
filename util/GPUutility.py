import win32com.client, psutil

def getGpuRamWindows():
    objWMI = win32com.client.GetObject("winmgmts:\\\\.\\root\\CIMV2")
    colItems = objWMI.ExecQuery("Select * from Win32_VideoController")
    GPUreal = 0
    GPUSlist = []
    for item in colItems:
        GPUlist = []
        GPUlist.append(f"{item.Name}")
        #print(f"Driver Version: {item.DriverVersion}")
        if item.AdapterRAM is not None:
            GPUlist.append(f"{item.AdapterRAM}")
        else:
            print("Adapter RAM: Not available")
        GPUSlist.append(GPUSlist)
        GPUreal =+ 1
        if GPUreal == 1: #change based on GPU amount
            break
    return GPUSlist