import win32com.client, psutil

def getGpuRamWindows():
    objWMI = win32com.client.GetObject("winmgmts:\\\\.\\root\\CIMV2")
    colItems = objWMI.ExecQuery("Select * from Win32_VideoController")
    GPUSlist = []
    for item in colItems:
        GPUlist = []
        GPUlist.append(f"{item.Name}")
        #print(f"Driver Version: {item.DriverVersion}")
        if item.AdapterRAM is not None:
            GPUlist.append(int(f"{item.AdapterRAM}"))
        else:
            GPUlist.append(None)
        GPUSlist.append(GPUlist)
    return GPUSlist

def getGpuLoadWindows():
    try:
        # Connect to WMI
        wmi = win32com.client.Dispatch("WbemScripting.SWbemLocator")
        wmi_service = wmi.ConnectServer(".", "root\\CIMV2")

        # Query GPU performance counters
        query = "SELECT * FROM Win32_PerfFormattedData_GPUPerformanceCounters_GPUEngine"
        items = wmi_service.ExecQuery(query)

        utilization_values = []

        for item in items:
            # Convert UtilizationPercentage to a float if not None
            if item.UtilizationPercentage is not None:
                try:
                    utilization = float(item.UtilizationPercentage)
                    utilization_values.append(utilization)
                except ValueError:
                    print(f"Skipping invalid utilization value: {item.UtilizationPercentage}")

        if utilization_values:
            # Consolidate metrics (average, sum, etc.)
            overall_load = sum(utilization_values) / len(utilization_values)
            return float(f"{overall_load}")
        else:
            return "No GPU utilization data found."

    except Exception as e:
        return f"Failed to get GPU load: {e}"