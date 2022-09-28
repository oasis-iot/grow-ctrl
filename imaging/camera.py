#---------------------------------------------------------------------------------------
#Manages Camera Timing & Image transmission
#---------------------------------------------------------------------------------------
import sys

#set proper path for modules
sys.path.append('/home/pi/oasis-grow')

#import libraries
import time
from subprocess import PIPE, Popen
from imaging import noir_ndvi
from utils import concurrent_state as cs
from utils import error_handler as err
from networking import db_tools as dbt

resource_name = "camera"

def take_picture(image_path, device_params):
    
    cs.check_lock(resource_name)
    cs.safety.lock(cs.lock_filepath, resource_name)

    if device_params["awb_mode"] == "on":
        #take picture and save to standard location: libcamera-still -e png -o test.png
        still = Popen(["raspistill", "-e", "jpg",  "-o", str(image_path)]) #snap: call the camera. "-w", "1920", "-h", "1080",
        still.communicate()
    else:
        still = Popen(["raspistill", "-e", "jpg",  "-o", str(image_path), "-awb", "off", "-awbg", device_params["awb_red"] + "," + device_params["awb_blue"]]) #snap: call the camera. "-w", "1920", "-h", "1080",
        still.communicate()

    cs.safety.unlock(cs.lock_filepath, resource_name)

def save_to_feed(image_path):
    #timestamp image
    timestamp = time.time()
    #move timestamped image into feed
    save_most_recent = Popen(["cp", str(image_path), "/home/pi/oasis-grow/data_out/image_feed/image_at_" + str(timestamp)+'.jpg'])
    save_most_recent.communicate()

def send_image(path):
    #send new image to firebase
    cs.load_state()
    user, db, storage = dbt.initialize_user(cs.structs["access_config"]["refresh_token"])
    dbt.store_file(user, storage, path, cs.structs["access_config"]["device_name"], "image.jpg")
    print("Sent image")

    #tell firebase that there is a new image
    dbt.patch_firebase(cs.structs["access_config"], "image_sent", "1")
    print("Firebase has an image in waiting")

#define a function to actuate element
def actuate(interval, nosleep = False): #amount of time between shots in minutes
    cs.load_state()

    take_picture('/home/pi/oasis-grow/data_out/image.jpg', cs.structs["device_params"])

    if cs.structs["feature_toggles"]["ndvi"] == "1":
        noir_ndvi.convert_image('/home/pi/oasis-grow/data_out/image.jpg')

    if cs.structs["feature_toggles"]["save_images"] == "1":
        save_to_feed('/home/pi/oasis-grow/data_out/image.jpg')

    if cs.structs["device_state"]["connected"] == "1":
        #send new image to firebase
        send_image('/home/pi/oasis-grow/data_out/image.jpg')

    if nosleep == True:
        return
    else:
        time.sleep(float(interval)*60) #once the physical resource itself is done being used, we can free it
                                       #not a big deal if someone actuates again while the main spawn is waiting
                                       #so long as they aren't doing so with malicious intent (would need DB or root access, make sure to turn off SSH or change your password)

if __name__ == '__main__':
    try:    
        actuate(str(sys.argv[1]))
    except KeyboardInterrupt:
        print("Interrupted")
        cs.safety.unlock(cs.lock_filepath, resource_name)
    except:
        print(err.full_stack())
        cs.safety.unlock(cs.lock_filepath, resource_name)
        


