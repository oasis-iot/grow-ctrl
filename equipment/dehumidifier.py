#---------------------------------------------------------------------------------------
#Manages Hardware for Dehumidifier
#---------------------------------------------------------------------------------------
#import shell modules
import sys

#set proper path for modules
sys.path.append('/home/pi/oasis-grow')

import RPi.GPIO as GPIO
import time

from utils import concurrent_state as cs

#get hardware config
cs.load_state()

#setup GPIO
GPIO.setmode(GPIO.BCM) #GPIO Numbers instead of board numbers
Dehum_GPIO = cs.structs["hardware_config"]["equipment_gpio_map"]["dehumidifier_relay"] #heater pin pulls from config file
GPIO.setup(Dehum_GPIO, GPIO.OUT) #GPIO setup
GPIO.output(Dehum_GPIO, GPIO.LOW) #relay open = GPIO.HIGH, closed = GPIO.LOW

#define a function making PID discrete & actuate element accordingly
def actuate_pid(dehum_ctrl):
    if (dehum_ctrl >= 0) and (dehum_ctrl < 1):
        #print("level 0")
        GPIO.output(Dehum_GPIO, GPIO.LOW) #off
        time.sleep(20)

    if (dehum_ctrl >= 1) and (dehum_ctrl < 10):
        #print("level 1")
        GPIO.output(Dehum_GPIO, GPIO.HIGH)
        time.sleep(2) #on
        GPIO.output(Dehum_GPIO, GPIO.LOW)
        time.sleep(18) #off

    if (dehum_ctrl >= 10) and (dehum_ctrl < 20):
        #print("level 2")
        GPIO.output(Dehum_GPIO, GPIO.HIGH)
        time.sleep(4) #on
        GPIO.output(Dehum_GPIO, GPIO.LOW)
        time.sleep(16) #off


    if (dehum_ctrl >= 20) and (dehum_ctrl < 30):
        #print("level 3")
        GPIO.output(Dehum_GPIO, GPIO.HIGH)
        time.sleep(6) #on
        GPIO.output(Dehum_GPIO, GPIO.LOW)
        time.sleep(16) #off

    if (dehum_ctrl >= 30) and (dehum_ctrl < 40):
        #print("level 4")
        GPIO.output(Dehum_GPIO, GPIO.HIGH)
        time.sleep(8) #on
        GPIO.output(Dehum_GPIO, GPIO.LOW)
        time.sleep(12) #off

    if (dehum_ctrl >= 40) and (dehum_ctrl < 50):
        #print("level 5")
        GPIO.output(Dehum_GPIO, GPIO.HIGH)
        time.sleep(10) #on
        GPIO.output(Dehum_GPIO, GPIO.LOW)
        time.sleep(10) #off

    if (dehum_ctrl >= 50) and (dehum_ctrl < 60):
        #print("level 6")
        GPIO.output(Dehum_GPIO, GPIO.HIGH)
        time.sleep(12) #on
        GPIO.output(Dehum_GPIO, GPIO.LOW)
        time.sleep(8) #off

    if (dehum_ctrl >= 60) and (dehum_ctrl < 70):
        #print("level 7")
        GPIO.output(Dehum_GPIO, GPIO.HIGH)
        time.sleep(14) #on
        GPIO.output(Dehum_GPIO, GPIO.LOW)
        time.sleep(6) #off

    if (dehum_ctrl >= 70) and (dehum_ctrl < 80):
        #print("level 8")
        GPIO.output(Dehum_GPIO, GPIO.HIGH)
        time.sleep(16) #on
        GPIO.output(Dehum_GPIO, GPIO.LOW)
        time.sleep(4) #off

    if (dehum_ctrl >= 80) and (dehum_ctrl < 90):
        #print("level 9")
        GPIO.output(Dehum_GPIO, GPIO.HIGH)
        time.sleep(18) #on
        GPIO.output(Dehum_GPIO, GPIO.LOW)
        time.sleep(2) #off

    if (dehum_ctrl >= 90) and (dehum_ctrl <= 100):
        #print("level 10")
        GPIO.output(Dehum_GPIO, GPIO.HIGH)
        time.sleep(20) #on
        GPIO.output(Dehum_GPIO, GPIO.LOW)
        time.sleep(0) #off

def actuate_interval(duration = 15, interval = 45): #amount of time between humidifier runs (seconds, seconds)
    GPIO.output(Dehum_GPIO, GPIO.HIGH)
    time.sleep(float(duration))
    GPIO.output(Dehum_GPIO, GPIO.LOW)
    time.sleep(float(interval))

if __name__ == '__main__':
    try:
        if cs.structs["feature_toggles"]["dehum_pid"] == "1":
            actuate_pid(float(sys.argv[1])) #trigger appropriate response
        else:
            actuate_interval(float(sys.argv[1]),float(sys.argv[2]))
    except KeyboardInterrupt:
        print("Interrupted")
    finally:    
        GPIO.cleanup()
