import sqlite3
import datetime as dt
import matplotlib.pyplot as plt; plt.rcdefaults()
import sys
import subprocess
import os
import netifaces as ni
import pytz

if(len(sys.argv) < 5 ) :
    print("Without required arguments. \nArg 1: Sensor name; \nArg 2: Upload techonology (Wifi or Lora); \nArg 3: Sliding window period (in minutes); \nArg 4: wireless upload interface ('wlan0' for RaspberryPi 4; 'wlan1' for RaspberryPi 3).")
    exit(0)


# Read InfluxDB Upload Configuration from 'InfluxDBConfiguration.db' database

try:
    conninflux= sqlite3.connect('/home/kali/Desktop/DB/InfluxDBConfiguration.db' , timeout=30)
    cinflux = conninflux.cursor()

    cinflux.execute("""SELECT * FROM InfluxDBConfiguration LIMIT 1""")
    influxDB_upload_config = cinflux.fetchall()

    cinflux.close()

except sqlite3.Error as error:
    print("Failed to read InfluxDB Upload configuration from local database.")

finally:
    if conninflux:
        conninflux.close()

if len(influxDB_upload_config) != 0:
    influxDB_IP_Address = influxDB_upload_config[0][0]
    influxDB_Org_Name = influxDB_upload_config[0][1]
    influxDB_Bucket_Name = influxDB_upload_config[0][2]
    influxDB_Auth_Token = influxDB_upload_config[0][3]
elif len(influxDB_upload_config) == 0:
    print("Failed to read InfluxDB Upload configuration from local database. Please make sure to \nconfigure an upload configuration by running the 'influxDBUploadConfig.py' script first.")
    exit(0)


sensorName = sys.argv[1]                    # Sensor name
uploadTechnology = sys.argv[2]              # Upload technology (Wifi or Lora)
slidingWindow = sys.argv[3]                 # Sliding window period, in minutes
wirelessUploadInterface = sys.argv[4]       # Wireless upload interface in case of upload via Wi-Fi (wlan1 -> RaspberryPi 4; wlan0 -> RaspberryPi 3) 

if not (uploadTechnology == "Wifi") and not (uploadTechnology == "Lora"):
    print("Argument 2 is not valid. Please enter 'Wifi' or 'Lora' for the upload technology.")
    exit(0)

if not slidingWindow.isdigit():
    print("Argument 3 is not a valid. Please enter the sliding window period, in minutes.")
    exit(0)

if not (wirelessUploadInterface == "wlan0" or wirelessUploadInterface == "wlan1"):
    print("Argument 4 is not valid. Please enter 'wlan1' for RaspberryPi 4 or 'wlan0' for RaspberryPi 3.")
    exit(0)


dataAtual=dt.datetime.now(pytz.utc).replace(tzinfo=None)
dataAnalizar= dataAtual - dt.timedelta(minutes=int(slidingWindow))

# Upload via Wi-Fi

if uploadTechnology == "Wifi":

    if len(ni.ifaddresses('eth0')) > 2: 
        uploadInterface='eth0'
    else:
        if len(ni.ifaddresses(str(wirelessUploadInterface))) > 2:        
            uploadInterface=wirelessUploadInterface

    ipAddress = ni.ifaddresses(uploadInterface)[ni.AF_INET][0]['addr']


    connwifi = sqlite3.connect('/home/kali/Desktop/DB/DeviceRecords.db' , timeout=30)
    cwifi = connwifi.cursor()

    # Device counting - Data packets

    cwifi.execute("""SELECT COUNT(*) FROM Data_Packets WHERE ((First_Record >= ? and First_Record <= ?) or (Last_Time_Found > ? and Last_Time_Found <= ?))""", (dataAnalizar, dataAtual, dataAnalizar, dataAtual))
    rows_data_packets = cwifi.fetchall()


    # Device counting - Probe Requests

    cwifi.execute("""SELECT COUNT(*) FROM Probe_Requests WHERE ((First_Record >= ? and First_Record <= ?) or (Last_Time_Found > ? and Last_Time_Found <= ?))""", (dataAnalizar, dataAtual, dataAnalizar, dataAtual))
    rows_probe_requests = cwifi.fetchall()


    detected_devices = rows_data_packets[0][0] + rows_probe_requests[0][0]


    # Send to InfluxDB

    #All
    cmd ="curl -i   --request POST \"http://" + str(influxDB_IP_Address) + ":8086/api/v2/write?org=" + str(influxDB_Org_Name) + "&bucket=" + str(influxDB_Bucket_Name) + "&precision=s\"  --header \"Authorization: Token " + str(influxDB_Auth_Token) + "\"  --header \"Content-Type: text/plain; charset=utf-8\"  --header \"Accept: application/json\" --data-binary 'numdetectionstable,device="+ sensorName + ",ipAddress=" + ipAddress + ",tecnology='wifi',type_data='all' devices_detected=" + str(detected_devices) + " " + str(int( ( (dataAtual) - dt.datetime(1970,1,1)).total_seconds())) + "'"   #Foi preciso adicionar "- dt.timedelta(minutes=60)" pois no Influx line protocol e usado um UTC timestamp, que nao e de acordo com o localtime do sensor (neste caso, e menos 1 hora GMT+1 (Potugal) -> GMT+0 (UTC))
    os.system(cmd)

    #Data Packets
    cmd ="curl -i   --request POST \"http://" + str(influxDB_IP_Address) + ":8086/api/v2/write?org=" + str(influxDB_Org_Name) + "&bucket=" + str(influxDB_Bucket_Name) + "&precision=s\"  --header \"Authorization: Token " + str(influxDB_Auth_Token) + "\"  --header \"Content-Type: text/plain; charset=utf-8\"  --header \"Accept: application/json\" --data-binary 'numdetectionstable,device="+ sensorName + ",ipAddress=" + ipAddress + ",tecnology='wifi',type_data='data_packets' devices_detected=" + str(rows_data_packets[0][0]) + " " + str(int( ( (dataAtual) - dt.datetime(1970,1,1)).total_seconds())) + "'"   #Foi preciso adicionar "- dt.timedelta(minutes=60)" pois no Influx line protocol e usado um UTC timestamp, que nao e de acordo com o localtime do sensor (neste caso, e menos 1 hora GMT+1 (Potugal) -> GMT+0 (UTC))
    os.system(cmd)

    #Probe Requests
    cmd ="curl -i   --request POST \"http://" + str(influxDB_IP_Address) + ":8086/api/v2/write?org=" + str(influxDB_Org_Name) + "&bucket=" + str(influxDB_Bucket_Name) + "&precision=s\"  --header \"Authorization: Token " + str(influxDB_Auth_Token) + "\"  --header \"Content-Type: text/plain; charset=utf-8\"  --header \"Accept: application/json\" --data-binary 'numdetectionstable,device="+ sensorName + ",ipAddress=" + ipAddress + ",tecnology='wifi',type_data='probe_requests' devices_detected=" + str(rows_probe_requests[0][0]) + " " + str(int( ( (dataAtual) - dt.datetime(1970,1,1)).total_seconds())) + "'"   #Foi preciso adicionar "- dt.timedelta(minutes=60)" pois no Influx line protocol e usado um UTC timestamp, que nao e de acordo com o localtime do sensor (neste caso, e menos 1 hora GMT+1 (Potugal) -> GMT+0 (UTC))
    os.system(cmd)


# Upload via LoRa

elif uploadTechnology == "Lora":

    print("The upload using the LoRaWAN protocol will be further available!")


