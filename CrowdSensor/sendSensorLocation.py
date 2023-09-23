import sqlite3
import datetime as dt
import pytz
import matplotlib.pyplot as plt; plt.rcdefaults()
import sys
import subprocess
import os

dataAtual=dt.datetime.now(pytz.utc).replace(tzinfo=None)

location = "A"

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
    
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


# Read input for sending sensor location measurement

print("Welcome! This script allows to set/alter the sensor location where it is currently deployed.")
print("IMPORTANT NOTE: If a sensor location was already sent with the same sensor name, the location \nof that sensor will be altered to this new location. \n")

sensorName = input("Please enter the sensor name: ")
print("The sensor name to set/alter the location is:", sensorName)

print("")


latitude = input("Please enter the latitude of the sensor: ")
longitude = input("Please enter the longitude of the sensor: ")

print("")

if not is_float(latitude):
    print("Latitude is not a valid number. Please try again.")
    exit(0)

if not is_float(longitude):
    print("Longitude is not a valid number. Please try again.")
    exit(0)


confirmation = input("The latitude and longitude (" + str(latitude + ", " + longitude) + ") will be set for the '" + str(sensorName) + "'. Are you sure? (Yes/No) ")

print("")

if confirmation == "Yes" or confirmation == "Y" or confirmation == "yes" or confirmation == "y":

    # Send sensor location to InfluxDB

    cmd ="curl -i   --request POST \"http://" + str(influxDB_IP_Address) + ":8086/api/v2/write?org=" + str(influxDB_Org_Name) + "&bucket=" + str(influxDB_Bucket_Name) + "&precision=s\"  --header \"Authorization: Token " + str(influxDB_Auth_Token) + "\"  --header \"Content-Type: text/plain; charset=utf-8\"  --header \"Accept: application/json\" --data-binary 'sensorLocation,device="+ sensorName + ",location=" + str(location) + " latitude="+ str(latitude) + ",longitude=" + str(longitude) + " " + str(int( (dataAtual - dt.datetime(1970,1,1)).total_seconds())) + "'"
    os.system(cmd)

    print("")

    print("Location for the '" + str(sensorName) + "' sensor sent to the cloud server.")

else:
    print("Sending refused. Exiting program.")
    exit(0)
