#!/usr/bin/python

import os
from time import sleep
import psutil
import glob

while True:
    virt = psutil.virtual_memory()
    if virt.percent >= 80:
        for fil in glob.glob("*.py"):
            os.system("killall -9 " + fil)
        for fil in glob.glob("*.pyc"):
            os.system("killall -9 " + fil)            
        os.system("killall -9 NW_C")
        os.system("killall -9 NWS_C")
        os.system("killall -9 NW_HS")
        os.system("killall -9 NWS_HS")
    sleep(0.5)
    print("Memory: ",virt.percent,"CPU: ",psutil.cpu_percent())
