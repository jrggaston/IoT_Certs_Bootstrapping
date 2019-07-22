# IoT_Certs_Bootstrapping

DISCLAIMER: This project is a proof of concept develop as part of a MSc in Cibersecurity, not intended for comercial use.

This projects tries to solve the problem of how the certificates are installed in the devices of an IoT Network.

The project consist of an ID server that receives the requests from the devices, generetes the certificates with its own CA, and deliver them to the devivces.

It is written in Python 2, and it has some dependecies:

- Bottle
- pyOpenssl
- hashlib
- socket
- mySQLdb
- random
- json

The comunication between the device and the server is done via HTTPS.

The server requeries the public and private key of its CA, and the certificate of the HTTPS server. Besides, it needs a database with the devices inventory.

The server is launched by executing $ python ID_server.py

On the other hand, the device needs to store its serial number, its factory date, and the IP and PORT of the server. 

The device starts the certificates request to the server by executing $ python IoT_Device.py
