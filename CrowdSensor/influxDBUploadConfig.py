import sqlite3
import sys

def validate_IP_address(ipAddress):
 
    for i in ipAddress:

        if i.isalpha():
            print("The IP address should only contain numbers. Please try again.")
            exit(0)

    dot_count = 0

    for i in ipAddress:

        if i == ".":
            dot_count += 1

    if dot_count != 3:
        print("The IP address is not in the correct syntax. Please try again.")
        exit(0)


    ip_list = list(map(str, ipAddress.split('.')))  
   
    for element in ip_list:  
        if int(element) < 0 or int(element) > 255 or (element[0]=='0' and len(element)!=1):  
            print("The IP address is not in the correct syntax. Please try again.")
            exit(0)

connwifi = sqlite3.connect('/home/kali/Desktop/DB/InfluxDBConfiguration.db', timeout=30)
cwifi = connwifi.cursor()


cloudServerIPAddress = input("Cloud Server IP Address: ")

validate_IP_address(cloudServerIPAddress)

influxDB_Org_Name = input("InfluxDB Organization name: ")
influxDB_Bucket = input("InfluxDB Bucket name: ")
authorization_Token = input("Authorization token: ")


try:

    cwifi.execute("""DELETE FROM InfluxDBConfiguration WHERE 1=1""")
    cwifi.execute("""INSERT INTO InfluxDBConfiguration (IP_Address, Org_Name, Bucket_Name, Auth_Token) VALUES(?, ?, ?, ?)""", (cloudServerIPAddress, influxDB_Org_Name, influxDB_Bucket, authorization_Token))
    connwifi.commit()
    cwifi.close()
    

except sqlite3.Error as error:
    print("Failed to save the InfluxDB configuration. Please try again.", error)

finally:
    if connwifi:
        connwifi.close()
        print("Done! The new InfluxDB upload configuration was correctly saved.")
        print("The sensor is ready for upload the crowding data to the cloud server with this new configuration.")

    