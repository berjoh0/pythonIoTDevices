import sys
sys.path.insert(0, '/home/pi/pythonIoTDevices')

from OneWire import DS18B20
tempJson = DS18B20.readTemps()
print(tempJson)