from os.path import exists
from generate_cert import generate_certificate, sign_certificate
from database import find_device_fd, save_data_into_device, get_challenge
from challenge import generate_random_number, resolve_challenge, check_challenge
import time
from bottle import get, post, request, run, response
from gevent import monkey
import json
import socket
import datetime



monkey.patch_all()

# function that waits to the requests of the devices.
# if a request is received, it gets the device id, and find it
# in the database. 
@post('/device_id')
def device_id():

    #get the device id from the post data
    postdata = request.body.read()        
    device_snr = request.forms.get("device_id")
    
    if (device_snr == None):
        print "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +  "] device_id not recevied"
        return

    #find the device in the database by reading the factory date
    try:
        factory_date = find_device_fd(device_snr)
    except:
	print "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +  "] Unable to connect with the database"
        return  
 
    if (factory_date != None):
    
        #if the device exists, generate the challenge, and save the solution
        challenge = generate_random_number()
        solution = resolve_challenge(device_snr, factory_date[0], challenge)

        #set a timeout of 5 minutes
        timeout = time.time() + 5*60
        try:
            save_data_into_device(solution, timeout, device_snr)
        except:
            print "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +  "] Unable to connect with the database"

        #send the challenge as response
        rv = { "challenge": challenge }
        response.content_type = 'application/json'
        return json.dumps(rv)
        
    else:
        #if there is no device do nothing
        print "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +  "] FD not found for device id: " + device_snr
        return
    

@post('/challenge_response')
def process_challenge_response():
    postdata = request.body.read()
    
    #get the post data - (device id and solution to the challenge)
    device_snr = request.forms.get("device_id")
    solution = request.forms.get("solved_challenge")

    if ((device_snr == None) or (solution == None)):
	print "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +  "] Not SNR or challenge received"
        return

    #get the data stored in the database to check if the rx data is ok
    try:
        data_stored = get_challenge(device_snr)
    except:
        print "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +  "] GET CHALLENGE: Error reading from DB."
        return

    try:
        solution_stored = data_stored[0][0]
        timeout = data_stored[0][1]
    except:
        print "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +  "] GET CHALLENGE: No data read from DB for snr " + device_snr
        return

    if ((solution_stored == None) or (timeout == None)):
        print "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +  "] No challenge stored for device id " + device_snr
        return

    #get the result 
    result = check_challenge(solution, solution_stored, timeout)
    if (result == True):
        #generate the certificates if the challenge received is ok
        try:
            private_key = generate_certificate("/tmp/", device_snr)
            certificate = sign_certificate("/tmp/", int(device_snr), 365*24*60*60, "/tmp")
        except:
            print "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +  "] Error generating certificates"
            return
        #create the json data to send
        rv = { "private_key": private_key, "device_cert": certificate }
    else:
        #if the result is not ok, send None
        rv = { "private_key": None , "device_cert": None }

    #send the response
    response.content_type = 'application/json'
    return json.dumps(rv)


#run the server
if (exists("/var/local/iot-bootstraping/server.crt") and exists("/var/local/iot-bootstraping/server.key")):
    run(host=socket.gethostbyname(socket.gethostname()), port=8443, server='gevent', certfile='/var/local/iot-bootstraping/server.cert', keyfile='/var/local/iot-bootstraping/server.key')
else:
    print "server certificate unknown"


