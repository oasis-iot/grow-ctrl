#must be run as root
#import shell modules
import sys

#set proper path for modules
sys.path.append('/home/pi/oasis-grow')

import board
import neopixel
import time
import multiprocessing
from utils import concurrent_state as cs

#get hardware config
cs.load_state()

num_leds = cs.hardware_config["onboard_led_config"]["num_leds"]

pixels = neopixel.NeoPixel(board.D21, num_leds)

#setup GPIO
#heater pin pulls from config file

def check_led_status():
    cs.load_state()
    if cs.device_state["led_status"] == "off":
        for x in range(0, num_leds-1):
            pixels[x] = (0, 0, 0)

    #Connected, Running (green, looping)
    if cs.device_state["led_status"] == "connected_running":
        for x in range(0, num_leds-1):
            pixels[x] = (0, 10, 0)
            time.sleep(0.04)
        for x in range(0, num_leds-1):
            pixels[x] = (0, 5, 0)
            time.sleep(0.04)   
    
    #Connected, Idle (green, still)
    if cs.device_state["led_status"] == "connected_idle":
        for x in range(0, num_leds-1):
            pixels[x] = (0, 5, 0)
            time.sleep(0.04)

    #Offline, Running (white, looping)
    if cs.device_state["led_status"] == "offline_running":
        for x in range(0, num_leds-1):
            pixels[x] = (10, 10, 10)
            time.sleep(0.04)
        for x in range(0, num_leds-1):
            pixels[x] = (5, 5, 5)
            time.sleep(0.04)   

    #Offline, Idle (white, still)
    if cs.device_state["led_status"] == "offline_idle":
        for x in range(0, num_leds-1):
            pixels[x] = (5, 5, 5)
            time.sleep(0.04)

    #Master sends error message (red, still)
    if cs.device_state["led_status"] == "error":
        for x in range(0, num_leds-1):
            pixels[x] = (5, 0, 0)
            time.sleep(0.04)

    #AP-mode, Server accepting connections (blue, looping)
    if cs.device_state["led_status"] == "accepting_wifi_connection":
        for x in range(0, num_leds-1):
            pixels[x] = (0, 0, 10)
            time.sleep(0.04)
        for x in range(0, num_leds-1):
            pixels[x] = (0, 0, 5)
            time.sleep(0.04)   

def run():
    def main_loop():
        while True:
            check_led_status()
            time.sleep(2.5)
    
    main_loop_process = multiprocessing.Process(target = main_loop)
    main_loop_process.start()

if __name__ == "__main__":
    #Desired Behavior: Calling led_start() reads the loop 
    #Test 
    #1. Start Process
    #2. Update LED States
    #3. Gracefully Exit
    pass