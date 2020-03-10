import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
args = "90"

Heat_GPIO = 17
GPIO.setup(Heat_GPIO, GPIO.OUT)

#take in temp PID 0-100 as args
tempCtrl = float(args)

#convert PID to discrete "levels"

if (tempCtrl >= 0) and (tempCtrl <= 1):
	#print("level 0")
	#off

if (tempCtrl >= 1) and (tempCtrl < 10):
	#print("level 1")
	#on for 1 off for 1

if (tempCtrl >= 10) and (tempCtrl < 20):
	#print("level 2")
	#on for 2, off for 1

if (tempCtrl >= 20) and (tempCtrl < 30):
	#print("level 3")
	#on for 3, off for 1

if (tempCtrl >= 30) and (tempCtrl < 40):
	#print("level 4")
	#on for 4, off for 1

if (tempCtrl >= 40) and (tempCtrl < 50):
	#print("level 5")
	#on for 5, off for 1

if (tempCtrl >= 50) and (tempCtrl < 60):
	#print("level 6")
	#on for 6, off for 1

if (tempCtrl >= 60) and (tempCtrl < 70):
	#print("level 7")
	#on for 7, off for 1

if (tempCtrl >= 70) and (tempCtrl < 80):
	#print("level 9")
	#on for 8, off for 1

if (tempCtrl >= 80) and (tempCtrl < 90):
	#print("level =9")
	#on for 9, off for 1

if (tempCtrl >= 90) and (tempCtrl <= 100):
	#print("level 10")
	#on
	GPIO.setup(Heat_GPIO, GPIO.OUT) # GPIO Assign mode
	GPIO.output(Heat_GPIO, GPIO.LOW) # out
	GPIO.output(Heat_GPIO, GPIO.HIGH) # on
