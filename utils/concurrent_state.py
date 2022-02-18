#This file contains tools for managing shared state in a python multiprocessing application
#Used in:
##main.py
##grow_ctrl.py
##update.py
##cameraElement.py

##oasis_setup(offline only)
##detect_db_events(offline only)


#import modules
import os
import os.path
import sys
import json

#set proper path for modules
sys.path.append('/home/pi/oasis-grow')
sys.path.append('/home/pi/oasis-grow/utils')
sys.path.append('/usr/lib/python37.zip')
sys.path.append('/usr/lib/python3.7')
sys.path.append('/usr/lib/python3.7/lib-dynload')
sys.path.append('/home/pi/.local/lib/python3.7/site-packages')
sys.path.append('/usr/local/lib/python3.7/dist-packages')
sys.path.append('/usr/lib/python3/dist-packages')

#declare state variables
device_state = None #describes the current state of the system
grow_params = None #describes the grow configuration of the system
hardware_config = None #holds hardware I/O setting & pin #s
access_config = None #contains credentials for connecting to firebase
feature_toggles = None #tells the system which features are in use

#declare state locking varibles
locks = None

def load_state(loop_limit=100000): #Depends on: 'json'; Modifies: device_state,hardware_config ,access_config
    global device_state, grow_params, access_config, feature_toggles, hardware_config

    #load device state
    for i in list(range(int(loop_limit))): #try to load, check if available, make unavailable if so, write state if so, write availabke iff so,  
        try:
            with open("/home/pi/oasis-grow/configs/device_state.json") as d:
                device_state = json.load(d) #get device state

            for k,v in device_state.items(): 
                if device_state[k] is None:
                    print("Read NoneType in device_state")
                    print("Resetting device_state...") 
                    reset_model.reset_device_state()
                else: 
                    pass    
        
            break
            
        except Exception as e:
            if i == int(loop_limit):
                reset_model.reset_device_state()
                print("Main.py tried to read max # of times. File is corrupted. Resetting device state ...")
            else:
                print("Main.py tried to read while file was being written. If this continues, file is corrupted.")
                pass
    
    #load grow_params
    for i in list(range(int(loop_limit))): #try to load, check if available, make unavailable if so, write state if so, write availabke iff so,  
        try:
            with open("/home/pi/oasis-grow/configs/grow_params.json") as g:
                grow_params = json.load(g) #get device state

            for k,v in grow_params.items(): 
                if grow_params[k] is None:
                    print("Read NoneType in grow_params")
                    print("Resetting grow_params...")
                    reset_model.reset_grow_params()
                     
                else: 
                    pass    
        
            break
            
        except Exception as e:
            if i == int(loop_limit):
                print("Main.py tried to read max # of times. File is corrupted. Resetting grow_params...")
                reset_model.reset_grow_params()
            else:
                print("Main.py tried to read while grow_params was being written. If this continues, file is corrupted.")
                pass   

    #load access_config
    for i in list(range(int(loop_limit))): #try to load, check if available, make unavailable if so, write state if so, write availabke iff so,  
        try:
            with open("/home/pi/oasis-grow/configs/access_config.json") as a:
                access_config = json.load(a) #get device state

            for k,v in access_config.items(): 
                if access_config[k] is None:
                    print("Read NoneType in access_config")
                    print("Resetting access_config...")
                    reset_model.reset_access_config()
                     
                else: 
                    pass    
        
            break
            
        except Exception as e:
            if i == int(loop_limit):
                print("Main.py tried to read max # of times. File is corrupted. Resetting access_config...")
                reset_model.reset_access_config()
            else:
                print("Main.py tried to read while access_config was being written. If this continues, file is corrupted.")
                pass               

    #load feature_toggles
    for i in list(range(int(loop_limit))): #try to load, check if available, make unavailable if so, write state if so, write availabke iff so,  
        try:
            with open("/home/pi/oasis-grow/configs/feature_toggles.json") as f:
                feature_toggles = json.load(f) #get device state

            for k,v in feature_toggles.items(): 
                if feature_toggles[k] is None:
                    print("Read NoneType in feature_toggles")
                    print("Resetting feature_toggles...")
                    reset_model.reset_feature_toggles()
                     
                else: 
                    pass    
        
            break
            
        except Exception as e:
            if i == int(loop_limit):
                print("Main.py tried to read max # of times. File is corrupted. Resetting feature_toggles...")
                reset_model.reset_feature_toggles()
            else:
                print("Main.py tried to read while feature_toggles was being written. If this continues, file is corrupted.")
                pass
            
    #load hardware_config
    for i in list(range(int(loop_limit))): #try to load, check if available, make unavailable if so, write state if so, write availabke iff so,  
        try:
            with open("/home/pi/oasis-grow/configs/hardware_config.json") as h:
                hardware_config = json.load(h) #get device state

            for k,v in hardware_config.items(): 
                if hardware_config[k] is None:
                    print("Read NoneType in hardware_config")
                    print("Resetting hardware_config...")
                    reset_model.reset_hardware_config()
                     
                else: 
                    pass    
        
            break
            
        except Exception as e:
            if i == int(loop_limit):
                print("Main.py tried to read max # of times. File is corrupted. Resetting hardware_config...")
                reset_model.reset_hardware_config()
            else:
                print("Main.py tried to read while hardware_config was being written. If this continues, file is corrupted.")
                pass
            
#modifies a firebase variable
def patch_firebase(field,value): #Depends on: load_state(),'requests','json'; Modifies: database['field'], state variables
    load_state()
    data = json.dumps({field: value})
    url = "https://oasis-1757f.firebaseio.com/"+str(access_config["local_id"])+"/"+str(access_config["device_name"])+".json?auth="+str(access_config["id_token"])
    result = requests.patch(url,data)

#gets the mutex
def load_locks(loop_limit = 10000):
    global locks
    for i in list(range(int(loop_limit))): #try to load, check if available, make unavailable if so, write state if so, write availabke iff so,  
        try:
            with open("/home/pi/oasis-grow/configs/locks.json","r+") as l:
                locks = json.load(l) #get locks

            for k,v in locks.items():
                if locks[k] is None:
                    print("Read NoneType in locks")
                    print("Resetting locks...")
                    reset_model.reset_locks()  
                else: 
                    pass
             
            break   
    
        except Exception as e:
            if i == int(loop_limit):
                print("Tried to load lock max number of times. File is corrupted. Resetting locks...")
                reset_model.reset_locks()
            else:
                print("Main.py tried to read while locks were being written. If this continues, file is corrupted.")
                pass

#closes down a file for exclusive access
def lock(file):
    global locks
    
    with open("/home/pi/oasis-grow/configs/locks.json", "r+") as l:
        locks = json.load(l) #get lock
        
        if file == "device_state":
            locks["device_state_write_available"] = "0" #let system know resource is not available
            l.seek(0)
            json.dump(locks, l)
            l.truncate()
                
        if file == "grow_params":
            locks["grow_params_write_available"] = "0" #let system know resource is not available
            l.seek(0)
            json.dump(locks, l)
            l.truncate()
            
        if file == "access_config":
            locks["access_config_write_available"] = "0" #let system know resource is not available
            l.seek(0)
            json.dump(locks, l)
            l.truncate()
    
        if file == "feature_toggles":
            locks["feature_toggles_write_available"] = "0" #let system know resource is not available
            l.seek(0)
            json.dump(locks, l)
            l.truncate()
        
        if file == "hardware_config":
            locks["hardware_config_write_available"] = "0" #let system know resource is not available
            l.seek(0)
            json.dump(locks, l)
            l.truncate()

#releases a file from exclusive access
def unlock(file):
    global locks
    
    with open("/home/pi/oasis-grow/configs/locks.json", "r+") as l:
        locks = json.load(l) #get lock
        
        if file == "device_state":
            locks["device_state_write_available"] = "1" #let system know resource is not available
            l.seek(0)
            json.dump(locks, l)
            l.truncate()
                
        if file == "grow_params":
            locks["grow_params_write_available"] = "1" #let system know resource is not available
            l.seek(0)
            json.dump(locks, l)
            l.truncate()
            
        if file == "access_config":
            locks["access_config_write_available"] = "1" #let system know resource is not available
            l.seek(0)
            json.dump(locks, l)
            l.truncate()
    
        if file == "feature_toggles":
            locks["feature_toggles_write_available"] = "1" #let system know resource is not available
            l.seek(0)
            json.dump(locks, l)
            l.truncate()
        
        if file == "hardware_config":
            locks["hardware_config_write_available"] = "1" #let system know resource is not available
            l.seek(0)
            json.dump(locks, l)
            l.truncate()
            
#save key values to .json
def write_state(path, field, value, loop_limit=100000, offline_only = False): #Depends on: load_state(), patch_firebase, 'json'; Modifies: path
    
    if offline_only == False:
        #these will be loaded in by the listener, so best to make sure we represent the change in firebase too
        if device_state["connected"] == "1": #write state to cloud
            try:
                patch_firebase(field,value)
            except Exception as e:
                print(e)
                pass

    for i in list(range(int(loop_limit))): #try to load, check if available, make unavailable if so, write state if so, write availabke iff so, 
        
        load_locks()
        
        try:
            with open(path, "r+") as x: # open the file.
                data = json.load(x) # can we load a valid json?

                if path == "/home/pi/oasis-grow/configs/device_state.json": #are we working in device_state?
                    if locks["device_state_write_available"] == "1": #check is the file is available to be written
                        lock("device_state")

                        data[field] = value #write the desired value
                        x.seek(0)
                        json.dump(data, x)
                        x.truncate()

                        unlock("device_state")
                        
                        load_state()
                        break #break the loop when the write has been successful

                    else:
                        pass
                    
                if path == "/home/pi/oasis-grow/configs/grow_params.json": #are we working in device_state?
                    if locks["grow_params_write_available"] == "1": #check is the file is available to be written
                        lock("grow_params")

                        data[field] = value #write the desired value
                        x.seek(0)
                        json.dump(data, x)
                        x.truncate()
            
                        unlock("grow_params")
                        
                        load_state()
                        break #break the loop when the write has been successful

                    else:
                        pass
                    
                if path == "/home/pi/oasis-grow/configs/access_config.json": #are we working in device_state?
                    if locks["access_config_write_available"] == "1": #check is the file is available to be written
                        lock("access_config")

                        data[field] = value #write the desired value
                        x.seek(0)
                        json.dump(data, x)
                        x.truncate()

                        unlock("access_config")
                        
                        load_state()
                        break #break the loop when the write has been successful

                    else:
                        pass
                    
                if path == "/home/pi/oasis-grow/configs/feature_toggles.json": #are we working in device_state?
                    if locks["feature_toggles_write_available"] == "1": #check is the file is available to be written
                        lock("feature_toggles")

                        data[field] = value #write the desired value
                        x.seek(0)
                        json.dump(data, x)
                        x.truncate()

                        unlock("feature_toggles")
                        
                        load_state()
                        break #break the loop when the write has been successful

                    else:
                        pass
                    
                if path == "/home/pi/oasis-grow/configs/hardware_config.json": #are we working in device_state?
                    if locks["hardware_config_write_available"] == "1": #check is the file is available to be written
                        lock("hardware_config")

                        data[field] = value #write the desired value
                        x.seek(0)
                        json.dump(data, x)
                        x.truncate()

                        unlock("hardware_config")
                        
                        load_state()
                        break #break the loop when the write has been successful

                    else:
                        pass

        except Exception as e: #If any of the above fails:
            if i == int(loop_limit):
                print("Tried to write state multiple times. File is corrupted. Resetting locks...")
                reset_model.reset_locks()
            else:
                print(e)
                print("Could not load locks. If this error persists, the lock file is corrupted. Retrying...")
                pass #continue the loop until write is successful or ceiling is hit