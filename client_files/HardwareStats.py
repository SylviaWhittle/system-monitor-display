import threading
import logging
import time
import wmi
from collections import defaultdict
import socket
import sys
import time
import datetime
import os
import json

# RUN this on the client machine, make sure to have Open Hardware Monitor running at the same time so that WMI can access the data.

# Create a defaultdict to store all the data inside
data = defaultdict()

# Create a WMI instance. WMI allows us to get the data that OpenHardwareMonitor is reporting.
w = wmi.WMI(namespace="root\OpenHardwareMonitor")

# The hostname for the server. If using an ip address, direcly assign this below.
server_hostname = "raspi4"
server_ip_address = socket.gethostbyname(server_hostname)
# The port that the data will be sent to
port = 5005

# Create socket for server
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
print("Running Sylvia's remote system monitor. Ctl-C to exit.")

# The data that we get from WMI is all in one huge dictionary, so we have to sift through it.
while True:
    info = w.Sensor()

    # This loop is great for finding the identifiers for the stats that we want.
    # Use this when trying to find stats that you want.
    # for item in info:
    #     print(item)

    # Aquire the data from the huge dictionary.
    for item in info:
        if item.Identifier == "/amdcpu/0/temperature/0":
            CPU_temp = item.Value
            data["CPU_temp"] = CPU_temp
            # print(f"CPU temp: {CPU_temp}")
        elif item.Identifier == "/amdcpu/0/load/0":
            CPU_load_total = item.value
            data["CPU_load_total"] = CPU_load_total
            # print(f"CPU load total: {CPU_load_total}")
        elif item.Identifier == "/amdcpu/0/load/1":
            CPU_load_1 = item.Value
            data["CPU_load_1"] = CPU_load_1
            # print(f"CPU load 1: {CPU_load_1}")
        elif item.Identifier == "/amdcpu/0/load/2":
            CPU_load_2 = item.Value
            data["CPU_load_2"] = CPU_load_2
            # print(f"CPU load 2: {CPU_load_2}")
        elif item.Identifier == "/amdcpu/0/load/3":
            CPU_load_3 = item.Value
            data["CPU_load_3"] = CPU_load_3
            # print(f"CPU load 3: {CPU_load_3}")
        elif item.Identifier == "/amdcpu/0/load/4":
            CPU_load_4 = item.Value
            data["CPU_load_4"] = CPU_load_4
            # print(f"CPU load 4: {CPU_load_4}")
        elif item.Identifier == "/amdcpu/0/load/5":
            CPU_load_5 = item.Value
            data["CPU_load_5"] = CPU_load_5
            # print(f"CPU load 5: {CPU_load_5}")
        elif item.Identifier == "/amdcpu/0/load/6":
            CPU_load_6 = item.Value
            data["CPU_load_6"] = CPU_load_6
            # print(f"CPU load 6: {CPU_load_6}")

        elif item.Identifier == "/ram/load/0":
            RAM_load = item.Value
            data["RAM_load"] = RAM_load
            # print(f"RAM load: {RAM_load}")
        elif item.Identifier == "/ram/data/0":
            RAM_used = item.Value
            data["RAM_used"] = RAM_used
            # print(f"RAM used: {RAM_used}")

        elif item.Identifier == "/nvidiagpu/0/load/0":
            GPU_load = item.Value
            data["GPU_load"] = GPU_load
            # print(f"GPU load: {GPU_load}")
        elif item.Identifier == "/nvidiagpu/0/load/4":
            GPU_RAM_load = item.Value
            data["GPU_RAM_load"] = GPU_RAM_load
            # print(f"GPU RAM load: {GPU_RAM_load}")
        elif item.Identifier == "/nvidiagpu/0/temperature/0":
            GPU_temperature = item.Value
            data["GPU_temperature"] = GPU_temperature
            # print(f"GPU temperature: {GPU_temperature}")

        elif item.Identifier == "/hdd/1/load/0":
            C_drive_load = item.Value
            data["C_drive_load"] = C_drive_load
            # print(f"C - drive load: {C_drive_load}")

        elif item.Identifier == "/hdd/0/load/0":
            D_drive_load = item.Value
            data["D_drive_load"] = D_drive_load
            # print(f"D - drive load: {D_drive_load}")

    # Send the data to the server
    sock.sendto(json.dumps(data).encode("utf-8"), (server_ip_address, port))

    # print(data)

    # Delay between sending the data
    time.sleep(1)
