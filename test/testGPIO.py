import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
print(GPIO.input(21))
##GPIO.output(21, GPIO.HIGH)
##time.sleep(10)
##GPIO.output(21, GPIO.LOW)
