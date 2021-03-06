#!/usr/bin/python
#Some basic code to send a serial number to Sumo - getting started with some basic logging.
import subprocess
import json
import sys

sys.path.append('/tmp')
from logtoSumo import logtoSumo

#Serial number function borrowed from @Frogor
def my_serial():
    return [x for x in [subprocess.Popen("system_profiler SPHardwareDataType |grep -v tray |awk '/Serial/ {print $4}'", shell=True, stdout=subprocess.PIPE).communicate()[0].strip()] if x]

def main():
    serial_number = my_serial()[0]
    logtoSumo(serial_number, "SimpleMDM install enterprise application command has triggered successfully.")


if __name__ == "__main__":
    main()
