#OneWire Class
#Johan Bergman

import json
import os
import re
import time

ow_path = '/sys/bus/w1/devices/'

def __init__():
    print("DS18B20 init")

def __readFiles():
    files = [name for name in os.listdir(ow_path)]
    if(len(files) == 0):
        time.sleep(30)
        # relaunch script
        __readFiles()
    else:
        temp_sensors = {"temperatureSensors":[]}
        for file in files:
            print("one wire file found: %s" % file)
            if(re.search("^28-[0-9a-z]{12}$", file)):
                temp_sensor = '%s%s/w1_slave' % (ow_path, file)
                print("temp_sensor:  %s" % temp_sensor)
                f = open(temp_sensor, 'r')
                lines = f.readlines()
                f.close()
                temp_output = lines[1].find('t=')
                if temp_output != 1:
                    temp_string = lines[1].strip()[temp_output + 2:]
                    temp_c = float(temp_string) / 1000.0
                    temp_sensors["temperatureSensors"].append({"id" : file, "temperature_C" : temp_c})

        return temp_sensors
    
def readTemps():
    tempLines = __readFiles()        
    return tempLines