import requests
from os.path import exists
import datetime
import json



server_cfg_path = "/var/local/id_server.cfg"

def get_server_cfg(path):
    port = 8443
    ip = "localhost"

    f= open(path,"r")

    for line in f:
        if "PORT" in line:
            line = line.strip()
            data = line.split("=")
            port = data[1]
        if "IP" in line:
            line = line.strip()
            data = line.split("=")
            ip = data[1]

    f.close()

    return ip, port

class iot_boot_class:
    def __init__(self):

        if (not (exists(server_cfg_path))):
            print "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +  "] No server configuration file found"
            exit()
    
        aux_ip, aux_port = get_server_cfg(server_cfg_path)

        self.ip = aux_ip
        self.port = aux_port
        self.private_key = ""
        self.public_cert = ""

    def send_device_cert_request(self, snr):
            

        payload = { 'device_id' : snr }

        try:
            url = "https://"+self.ip+":"+str(self.port)+"/device_id"
            #r = requests.post("https://63.35.171.25:8443/device_id", data=payload, verify = False)
            r = requests.post(url, data=payload, verify = False)
        except:
            print "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +  "] Unable to connect to the server"
            return -1 
            
        
        try:
            data = r.text
            rx_data = json.loads(data)
        except:
            print "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +  "] Wrong data format received. Wrong request or unknown snr"
            return -2
            

        #get challenge
        try:
            challenge = rx_data["challenge"]
        except:
            print "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +  "] No challenge received"
            return -3

        return challenge

    def send_challenge_response(self, snr, solution):
            

        payload = { 'device_id' : snr, 'solved_challenge' : solution }

        try:
            url = "https://"+self.ip+":"+str(self.port)+"/challenge_response"
            r = requests.post(url, data=payload, verify = False)
        except:
            print "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +  "] Unable to send the challenge response to the server"
            return -4
            
        
        #recieve certificates
        try:
            certificates = r.text
            rx_data = json.loads(certificates)
        except:
            print "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +  "] Certificates not received: Wrong response format"
            return -5
            

        try:
            #if received, save the certificates
            if ((rx_data["private_key"] != None) and (rx_data["device_cert"])):
                self.private_key = rx_data["private_key"]
                self.public_cert = rx_data["device_cert"]
                return 0
            else:
                print "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +  "] wrong challenge solution"
                return -6
        except:
            print "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +  "] No certificates received"
            return -7
            




