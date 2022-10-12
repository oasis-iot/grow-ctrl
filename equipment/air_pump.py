#---------------------------------------------------------------------------------------
#Manages Hardware for Lighting
#---------------------------------------------------------------------------------------

#import shell modules
import sys
import signal

#set proper path for modules
sys.path.append('/home/pi/oasis-grow')

import rusty_pins
from peripherals import relays
from utils import concurrent_state as cs
from utils import error_handler as err

resource_name = "air_pump"
cs.check_lock(resource_name)

#setup GPIO
cs.load_state()
air_GPIO = int(cs.structs["hardware_config"]["equipment_gpio_map"]["air_relay"]) #heater pin pulls from config file
pin = rusty_pins.GpioOut(air_GPIO)

def clean_up(*args):
    cs.safety.unlock(cs.lock_filepath, resource_name)
    pin.set_low()
    sys.exit()

if __name__ == '__main__':
    
    signal.signal(signal.SIGTERM,clean_up)
    try:
        print("Turning air pump on at " + sys.argv[1] + ":00 and off at " + sys.argv[2] + ":00, refreshing every " + sys.argv[3] + " minutes...")
        relays.actuate_time_hod(pin, int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), interval_units = "minutes")
    except KeyboardInterrupt:
        print("Air pump was interrupted")
    except Exception:
        print("Air pump ncountered an error!")
        print(err.full_stack())
    finally:
        clean_up()


