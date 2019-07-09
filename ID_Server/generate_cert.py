from OpenSSL import crypto, SSL
from socket import gethostname
from time import  time, mktime
from os.path import join

def generate_certificate(output_path, snr):
    
    # generate the private key
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)

    data = crypto.dump_privatekey(crypto.FILETYPE_PEM, key)
    open(join(output_path, "device_private.key"), "wt").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))

    #geport gmtinerate the sign request
    req = crypto.X509Req()
    req.get_subject().CN = gethostname()
    req.get_subject().C = "ES"
    req.get_subject().ST = "Zaragoza"
    req.get_subject().L = "Zaragoza"
    req.get_subject().O = "myorg"
    req.get_subject().OU = "myorg"
    req.get_subject().commonName = snr
    #req.get_subject().serial_number(int(snr))
    req.set_pubkey(key)
    req.sign(key, "sha256")

    open(join(output_path, "device.csr"), "wt").write(crypto.dump_certificate_request(crypto.FILETYPE_PEM, req))

    return data

    

def sign_certificate(input_path, serial_number, valid_time, output_path):

    # get the device
    deviceCsr = crypto.load_certificate_request(crypto.FILETYPE_PEM, open(join(input_path, "device.csr"), 'rb').read()) 
    #get the CAroot.key
    CAprivatekey = crypto.load_privatekey(crypto.FILETYPE_PEM, open( "rootCA.key", 'rb').read(), "mastercs") 
    #get the rootCA.pem
    caCert = crypto.load_certificate(crypto.FILETYPE_PEM, open("rootCA.pem", 'rb').read()) 

    cert = crypto.X509()
    cert.set_serial_number(serial_number)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(valid_time)
    cert.set_issuer(caCert.get_subject())
    cert.set_subject(deviceCsr.get_subject())
    cert.set_pubkey(deviceCsr.get_pubkey())
    cert.sign(CAprivatekey, 'sha256')

    open(join(output_path, "device_test.crt"), "wt").write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

    data = crypto.dump_certificate(crypto.FILETYPE_PEM, cert) + open("rootCA.pem", 'rb').read()
    
    return data




