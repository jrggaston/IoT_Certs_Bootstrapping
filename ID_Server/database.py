import MySQLdb


def find_device_fd(snr):
    
    db = MySQLdb.connect(host="localhost",  # host of the database
                     user="root",       	# username
                     passwd="",     		# password
                     db="devices_database")	# name of the database

    # Create a Cursor object to execute queries.
    cur = db.cursor()
    
    #find from testdevices table a device with the snr received as argument
    cmd = "SELECT fd from devices WHERE snr="+ str(snr)
    cur.execute(cmd)

    fd = cur.fetchone()	
    
    cur.close()
    db.close()

    return fd


def save_data_into_device(challenge, timeout, snr):
    db = MySQLdb.connect(host="localhost",  # your host 
                     user="root",           # username
                     passwd="",             # password
                     db="devices_database")       # name of the database

   # Create a Cursor object to execute queries.
    cur = db.cursor()

    cmd = "UPDATE devices SET timeout=" +str(timeout) +" WHERE snr=" + str(snr)
    cur.execute(cmd)
    cmd = "UPDATE devices SET solution='" + str(challenge) + "' WHERE snr=" + str(snr)
    cur.execute(cmd)
    db.commit()

    cur.close()
    db.close()
   
    return


def get_challenge(snr):

    db = MySQLdb.connect(host="localhost",  # your host 
                     user="root",           # username
                     passwd="",             # password
                     db="devices_database")       # name of the database

   # Create a Cursor object to execute queries.
    cur = db.cursor()

    cmd = "SELECT solution,timeout from devices WHERE snr="+ str(snr)
    cur.execute(cmd)

    data = cur.fetchall()

    cur.close()
    db.close()

    return data






