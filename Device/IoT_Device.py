from os.path import exists
import hashlib
import time
import random
import iot_boot_api
import json
import datetime

private_key_path = "/usr/local/certs/device_key.key"
certificate_path = "/usr/local/certs/device_cert.crt"
snr_path = "/var/local/snr"
fd_path = "/var/local/fd"

#function to calculate the hash that solves the challenge.
def resolve_challenge(snr, factory_date, challenge):

   aux = str(snr) + str(factory_date) + str(challenge)
   hash = hashlib.sha256(aux).hexdigest()

   return hash


#function to find a file:
# returns TRUE if the file exists, otherwise FALSE
def find_file(path_to_file):
   if (exists(path_to_file)):
      return True
   else:
      return False 

def get_data(path):
    f= open(path,"r")
    
    content = f.readlines()
    snr = content[0]
    f.close()
    return snr.strip()

def save_content_into_file(data_to_write, path_to_file):
    f= open(path_to_file,"w")
    f.write(str(data_to_write))
    f.close()
    return

#Look if the device has certificates
if (find_file(private_key_path) == False or find_file(certificate_path) == False):
    #get the serial number of the device   
    if (not find_file(snr_path)):
        print "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +  "] No SNR file found"
        exit()
    if (not find_file(fd_path)):
        print "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +  "] No FD file found"
        exit()

    snr = get_data(snr_path)
    fd = get_data(fd_path)
    
    #send request to the server
    iot_api = iot_boot_api.iot_boot_class()

    certs_received = False
    while (not certs_received):

 
        challenge = iot_api.send_device_cert_request(snr)
        if (challenge < 0):
            print "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +  "] No challenge received"
            time.sleep(60)
            continue
    
        #resolve challenge
        solution = resolve_challenge(snr, fd, challenge)

        if (iot_api.send_challenge_response(snr, solution) == 0):
            private_key = iot_api.private_key
            public_cert = iot_api.public_cert
        else:
            print "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +  "] No certificates received"
            time.sleep(60)
            continue
           
        #if received, save the certificates
        if ((private_key != None) and (public_cert != None)):
            save_content_into_file(private_key, private_key_path)
            save_content_into_file(public_cert, certificate_path)  
            certs_received = True
        else:
            print "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +  "] wrong challenge solution"
            time.sleep(60)
            continue
        

