import sqlite3
import datetime as dt

dataAnalizar=dt.datetime.now() - dt.timedelta(minutes=2)

#Eliminacao dos registos Wifi antigos

connwifi = sqlite3.connect('/home/kali/Desktop/DB/Test.db', timeout=30)
cwifi = connwifi.cursor()
cwifi.execute('DELETE FROM WifiDump where 1=1')
connwifi.commit()
cwifi.execute('DELETE FROM Cellphone_Records_15  where Last_Time_Found < ?',( dataAnalizar , ))
connwifi.commit()
cwifi.execute('DELETE FROM Cellphone_Records_30 where Last_Time_Found < ?',( dataAnalizar , ))
connwifi.commit()

#Eliminacao dos registos Bluetooth antigos

connbluetooth = sqlite3.connect('/home/kali/Desktop/DB/project.db', timeout=30)
cbluetooth = connbluetooth.cursor()
cbluetooth.execute('DELETE FROM Cellphone_Records where Last_Time_Found < ?',( dataAnalizar , ))
connbluetooth.commit()

