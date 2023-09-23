import sqlite3
import sys

coninflux = sqlite3.connect('/home/kali/Desktop/DB/InfluxDBConfiguration.db', timeout=30)
cinflux = coninflux.cursor()

cinflux.execute("""SELECT * FROM InfluxDBConfiguration""")
influxDB_upload_config = cinflux.fetchall()

if len(influxDB_upload_config) == 0:
    print("There is not active InfluxDB Upload Configuration. \nPlease first configure it by running the 'influxDBUploadConfig.py' script.")
    exit(0)

print("The active InfluxDB Upload Configuration is: \n")

print("Cloud Server IP Address: " + str(influxDB_upload_config[0][0]))
print("InfluxDB Organization Name: " + str(influxDB_upload_config[0][1]))
print("InfluxDB Bucket Name: " + str(influxDB_upload_config[0][2]))
print("InfluxDB Authorization Token: " + str(influxDB_upload_config[0][3]))

cinflux.close()

