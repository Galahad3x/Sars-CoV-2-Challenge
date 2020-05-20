import os
from time import sleep
import psutil

while True:
    virt = psutil.virtual_memory()
    if virt.percent >= 80:
        os.system("killall -9 python3")
        os.system("killall -9 NW_C")
        os.system("killall -9 NWS_C")
        os.system("killall -9 NW_HS")
        os.system("killall -9 NWS_HS")
    sleep(0.5)
    print("Memory: ",virt.percent,"CPU: ",psutil.cpu_percent())
