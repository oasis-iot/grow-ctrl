#import shell modules
import sys

#set proper path for modules
sys.path.append('/home/pi/oasis-grow')

#data handling
import re
import time

#import custom modules
from utils import reset_model
from utils import slow_concurrent_state as slow_cs
from utils import error_handler as err
from networking import wifi

#create a password-protected lan interface for accepting credentials
import streamlit as st

#update wpa_supplicant.conf
def modWiFiConfig(SSID, password):
    config_lines = [
    'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev',
    'update_config=1',
    'country=US',
    '\n',
    'network={',
    '\tssid="{}"'.format(SSID),
    '\tpsk="{}"'.format(password),
    '\tkey_mgmt=WPA-PSK',
    '}'
    ]

    config = '\n'.join(config_lines)
    #print(config)

    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "r+") as w:
        w.seek(0)
        w.write(config)
        w.truncate()

    print("WiFi configs added")

#update access_config.json
def modAccessConfig(name, e, p):
    slow_cs.structs["access_config"] = {}
    slow_cs.structs["access_config"]["device_name"] = str(name)
    slow_cs.structs["access_config"]["wak"] = "AIzaSyBPuJwU--0ZlvsbDV9LmKJdYIljwNwzmVk"
    slow_cs.structs["access_config"]["e"] = str(e)
    slow_cs.structs["access_config"]["p"] = str(p)
    slow_cs.structs["access_config"]["refresh_token"] = " "
    slow_cs.structs["access_config"]["id_token"] = " "
    slow_cs.structs["access_config"]["local_id"] = " "

    slow_cs.write_dict("/home/pi/oasis-grow/configs/access_config.json", slow_cs.structs["access_config"], db_writer = None)

    print("Access configs added")

def save_creds_exit(email, password, wifi_name, wifi_pass, device_name, cmd = False):
    
    device_name = re.sub('[^a-zA-Z0-9\n\.]', ' ', device_name) #sub all non-alphaneumeric characters with spaces
    device_name - device_name.replace(" ","-") #sub all spaces with dashes

    #place credentials in proper locations
    modWiFiConfig(wifi_name, wifi_pass)
    print("Wifi creds added")
    modAccessConfig(device_name, email, password)
    print("Access creds added")
    
    st.success("Added WiFi & access credentials to device. Please reconnect computer to internet, leave this page, and log back into https://dashboard.oasis-gardens.io. If successful, you will see the device name appear under 'Your Fleet.'")
    
    #reset_box
    reset_model.reset_device_state()

    #set new_device to "1" before rebooting
    slow_cs.write_state("/home/pi/oasis-grow/configs/device_state.json", "new_device", "1", db_writer = None)

    if cmd == False: #pass this argument as true to save creds without rebooting
        #stand up wifi and reboot
        wifi.enable_wifi()

if __name__ == '__main__':

    default = ""

    st.title('Oasis Device Setup')

    email = st.text_input('Oasis Email', default)

    password = st.text_input('Oasis Password', default, type="password")

    wifi_name = st.text_input('Wifi Name', default)

    wifi_pass = st.text_input('Wifi Password', default, type="password")

    device_name = st.text_input('Name this device:', default)

    #st.button('Launch', on_click=save_creds_exit, args=[email, password, wifi_name, wifi_pass, device_name]) #only for recent streamlit versions

    if st.button("Launch"):
        try:
            save_creds_exit(email, password, wifi_name, wifi_pass, device_name)
            time.sleep(1)
        except:
            print(err.full_stack())
            sys.exit()