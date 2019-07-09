# IoT_Certs_Bootstrapping

DISCLAIMER: This project is a proof of concept develop as part of a MSc in Cibersecurity, not intended for comercial use.

This projects tries to solve the problem how the certificates are installed in the devices of an IoT Network.

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

The server requeries the certificates of its CA, and the certificate of the HTTPS server. Besides, it needs a database with the devices inventory.

On the other hand, the device need to store it serial number, its factory date, and the IP and PORT of the server. 
