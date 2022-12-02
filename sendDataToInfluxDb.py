import sqlite3
import datetime as dt
import matplotlib.pyplot as plt; plt.rcdefaults()
import sys
import subprocess
import os
import netifaces as ni
from gpiozero import CPUTemperature

cpu = CPUTemperature()
cpuTemp = int(cpu.temperature)


if(len(sys.argv) <5 ) :
    print("sem os argumentos necessarios")
    exit(0)

wifiBol=int(sys.argv[1])
bluetoothBol=int(sys.argv[2])
cpuTempBol=int(sys.argv[3])
deviceName=sys.argv[4]
ipAddress = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
macAddress = ni.ifaddresses('eth0')[ni.AF_LINK][0]['addr']

dataAtual=dt.datetime.now()
dataAnalizar=dt.datetime.now() - dt.timedelta(minutes=15)

# Dados Wifi

if(wifiBol==1) :


    connwifi = sqlite3.connect('/home/kali/Desktop/DB/Test.db' , timeout=30)
    cwifi = connwifi.cursor();

    # instante timinng

    cwifi.execute('select count(*) from Cellphone_Records_15 where (First_Record >= ? and First_Record <= ?) or (Last_Time_Found > ? and Last_Time_Found <= ?)' , (dataAnalizar, dataAtual, dataAnalizar, dataAtual))
    rows = cwifi.fetchall();
    #print(rows)

    cwifi.execute('select count(*) from Cellphone_Records_15 where ((First_Record >= ? and First_Record <= ?) or (Last_Time_Found > ? and Last_Time_Found <= ?)) and ID NOT LIKE "_2%" and ID NOT LIKE "_6%" and ID NOT LIKE "_A%" and ID NOT LIKE "_E%"  ' , (dataAnalizar, dataAtual, dataAnalizar, dataAtual))
    rows_no_randoms = cwifi.fetchall();

    cwifi.execute( 'select count(*) from Cellphone_Records_15 where ((First_Record >= ? and First_Record <= ?) or (Last_Time_Found > ? and Last_Time_Found <= ?)) and (ID LIKE "_2%" or ID LIKE "_6%" or ID LIKE "_A%" or ID LIKE "_E%"  )',(dataAnalizar, dataAtual, dataAnalizar, dataAtual))
    rows_only_randoms = cwifi.fetchall();

    # Envio para InfluxDb

    #print ("curl -i  --request POST \"http://194.210.120.41:8086/api/v2/write?org=TomasWorkspace&bucket=DetectionsDB&precision=s\"  --header \"Authorization: Token PnyTV3BaonLB7-pTpKsuvUySrPLRn12OnORqIHwby3HVJiaUxy9XSqI1ByitibVaan9wNXxdaLZvh8ECp5WU5w==\"  --header \"Content-Type: text/plain; charset=utf-8\"  --header \"Accept: application/json\" --data-binary 'numdetectionstable,device="+ deviceName + ",ipaddress=" + ipAddress + ",macAddress=" + macAddress + ",tecnology='wifi',type_data='all' numdetections=" + str(rows[0][0]) + " " + str(int( (dataAtual - dt.datetime(1970,1,1)).total_seconds())) + "'")
    cmd ="curl -i   --request POST \"http://194.210.120.41:8086/api/v2/write?org=TomasWorkspace&bucket=DetectionsDB&precision=s\"  --header \"Authorization: Token PnyTV3BaonLB7-pTpKsuvUySrPLRn12OnORqIHwby3HVJiaUxy9XSqI1ByitibVaan9wNXxdaLZvh8ECp5WU5w==\"  --header \"Content-Type: text/plain; charset=utf-8\"  --header \"Accept: application/json\" --data-binary 'numdetectionstable,device="+ deviceName + ",ipaddress=" + ipAddress + ",macAddress=" + macAddress + ",tecnology='wifi',type_data='all' numdetections=" + str(rows[0][0]) + " " + str(int( (dataAtual - dt.datetime(1970,1,1)).total_seconds())) + "'"
    os.system(cmd)
    
    #print ("curl -i --request POST \"http://194.210.120.41:8086/api/v2/write?org=TomasWorkspace&bucket=DetectionsDB&precision=s\"  --header \"Authorization: Token PnyTV3BaonLB7-pTpKsuvUySrPLRn12OnORqIHwby3HVJiaUxy9XSqI1ByitibVaan9wNXxdaLZvh8ECp5WU5w==\"  --header \"Content-Type: text/plain; charset=utf-8\"  --header \"Accept: application/json\" --data-binary 'numdetectionstable,device="+ deviceName + ",ipaddress=" + ipAddress + ",tecnology='wifi',type_data='no_randoms' numdetections=" + str(rows_no_randoms[0][0]) + " " + str(int( (dataAtual - dt.datetime(1970,1,1)).total_seconds())) + "'")
    cmd ="curl -i --request POST \"http://194.210.120.41:8086/api/v2/write?org=TomasWorkspace&bucket=DetectionsDB&precision=s\"  --header \"Authorization: Token PnyTV3BaonLB7-pTpKsuvUySrPLRn12OnORqIHwby3HVJiaUxy9XSqI1ByitibVaan9wNXxdaLZvh8ECp5WU5w==\"  --header \"Content-Type: text/plain; charset=utf-8\"  --header \"Accept: application/json\" --data-binary 'numdetectionstable,device="+ deviceName + ",ipaddress=" + ipAddress + ",macAddress=" + macAddress + ",tecnology='wifi',type_data='no_randoms' numdetections=" + str(rows_no_randoms[0][0]) + " " + str(int( (dataAtual - dt.datetime(1970,1,1)).total_seconds())) + "'"
    os.system(cmd)
    
    #print ("curl -i --request POST \"http://194.210.120.41:8086/api/v2/write?org=TomasWorkspace&bucket=DetectionsDB&precision=s\"  --header \"Authorization: Token PnyTV3BaonLB7-pTpKsuvUySrPLRn12OnORqIHwby3HVJiaUxy9XSqI1ByitibVaan9wNXxdaLZvh8ECp5WU5w==\"  --header \"Content-Type: text/plain; charset=utf-8\"  --header \"Accept: application/json\" --data-binary 'numdetectionstable,device="+ deviceName + ",ipaddress=" + ipAddress + ",tecnology='wifi',type_data='only_randoms' numdetections=" + str(rows_only_randoms[0][0]) + " " + str(int( (dataAtual - dt.datetime(1970,1,1)).total_seconds())) + "'")
    cmd="curl -i --request POST \"http://194.210.120.41:8086/api/v2/write?org=TomasWorkspace&bucket=DetectionsDB&precision=s\"  --header \"Authorization: Token PnyTV3BaonLB7-pTpKsuvUySrPLRn12OnORqIHwby3HVJiaUxy9XSqI1ByitibVaan9wNXxdaLZvh8ECp5WU5w==\"  --header \"Content-Type: text/plain; charset=utf-8\"  --header \"Accept: application/json\" --data-binary 'numdetectionstable,device="+ deviceName + ",ipaddress=" + ipAddress + ",macAddress=" + macAddress + ",tecnology='wifi',type_data='only_randoms' numdetections=" + str(rows_only_randoms[0][0]) + " " + str(int( (dataAtual - dt.datetime(1970,1,1)).total_seconds())) + "'"
    os.system(cmd)


    """
    #Tempo de permanencia medio

    cwifi.execute('select sum( (JulianDay(Last_Time_Found) - JulianDay(First_Record))  * 24 * 60   ) from Cellphone_Records_15 where ((First_Record >= ? and First_Record <= ?) or (Last_Time_Found > ? and Last_Time_Found <= ?)) ', (dataAnalizar, dataAtual, dataAnalizar, dataAtual))
    rows_tpm = cwifi.fetchall();

    if(rows_tpm[0][0] != None):
        #print ("curl -i -XPOST \"https://sniff.iscte.me/write?db=mydb&precision=s\" --data-binary 'medianstayngtime,device="+ deviceName + ",tecnology='wifi',type_data='all' medianstayngtime=" + str(rows_tpm[0][0] / rows[0][0]) + " " + str(int( (dataAnalizar - dt.datetime(1970,1,1)).total_seconds())) + "'")
        cmd="curl -i --request POST \"http://194.210.120.41:8086/api/v2/write?org=InfluxDbCrowding&bucket=DetectionsDB&precision=s\"  --header \"Authorization: Token Kk2s4LBWEs_uQd3KiyVhMWsOmijSv16S3p8xZOGMTti5FnQCO4YTNS-UfCzAeUoPJNb2c5vTg6DEQ7tvkCdveg==\"  --header \"Content-Type: text/plain; charset=utf-8\"  --header \"Accept: application/json\" --data-binary 'medianstayngtime,device="+ deviceName + ",ipaddress=" + ipAddress + ",tecnology='wifi',type_data='all' medianstayngtime=" + str( float(rows_tpm[0][0]) / float(rows[0][0])) + " " + str(int( (dataAtual - dt.datetime(1970,1,1)).total_seconds())) + "'"
        os.system(cmd)
    
    else:
        #print ("curl -i -XPOST \"https://sniff.iscte.me/write?db=mydb&precision=s\" --data-binary 'medianstayngtime,device="+ deviceName + ",tecnology='wifi',type_data='all' medianstayngtime=" + str(0) + " " + str(int( (dataAnalizar - dt.datetime(1970,1,1)).total_seconds())) + "'")
        cmd="curl -i --request POST \"http://194.210.120.41:8086/api/v2/write?org=InfluxDbCrowding&bucket=DetectionsDB&precision=s\"  --header \"Authorization: Token Kk2s4LBWEs_uQd3KiyVhMWsOmijSv16S3p8xZOGMTti5FnQCO4YTNS-UfCzAeUoPJNb2c5vTg6DEQ7tvkCdveg==\"  --header \"Content-Type: text/plain; charset=utf-8\"  --header \"Accept: application/json\" --data-binary 'medianstayngtime,device=" + deviceName + ",ipaddress=" + ipAddress + ",tecnology='wifi',type_data='all' medianstayngtime=" + str(0) + " " + str(int((dataAtual - dt.datetime(1970, 1, 1)).total_seconds())) + "'"
        os.system(cmd)


    cwifi.execute( 'select sum( (JulianDay(Last_Time_Found) - JulianDay(First_Record))  * 24 * 60   ) from Cellphone_Records_15 where ((First_Record >= ? and First_Record <= ?) or (Last_Time_Found > ? and Last_Time_Found <= ?)) and ID NOT LIKE "_2%" and ID NOT LIKE "_6%" and ID NOT LIKE "_A%" and ID NOT LIKE "_E%"  ',
        (dataAnalizar, dataAtual, dataAnalizar, dataAtual))
    rows_tpm_no_randoms = cwifi.fetchall();
    if (rows_tpm_no_randoms[0][0] != None):
        #print("curl -i -XPOST \"https://sniff.iscte.me/write?db=mydb&precision=s\" --data-binary 'medianstayngtime,device=" + deviceName + ",tecnology='wifi',type_data='no_randoms' medianstayngtime=" + str(rows_tpm_no_randoms[0][0] / rows_no_randoms[0][0]) + " " + str(int((dataAnalizar - dt.datetime(1970, 1, 1)).total_seconds())) + "'")
        cmd ="curl -i --request POST \"http://194.210.120.41:8086/api/v2/write?org=InfluxDbCrowding&bucket=DetectionsDB&precision=s\"  --header \"Authorization: Token Kk2s4LBWEs_uQd3KiyVhMWsOmijSv16S3p8xZOGMTti5FnQCO4YTNS-UfCzAeUoPJNb2c5vTg6DEQ7tvkCdveg==\"  --header \"Content-Type: text/plain; charset=utf-8\"  --header \"Accept: application/json\" --data-binary 'medianstayngtime,device=" + deviceName + ",ipaddress=" + ipAddress + ",tecnology='wifi',type_data='no_randoms' medianstayngtime=" + str(float(rows_tpm_no_randoms[0][0]) / float(rows_no_randoms[0][0])) + " " + str(int((dataAtual - dt.datetime(1970, 1, 1)).total_seconds())) + "'"
        os.system(cmd)

    else:
        #print("curl -i -XPOST \"https://sniff.iscte.me/write?db=mydb&precision=s\" --data-binary 'medianstayngtime,device=" + deviceName + ",tecnology='wifi',type_data='no_randoms' medianstayngtime=" + str(0) + " " + str(int((dataAnalizar - dt.datetime(1970, 1, 1)).total_seconds())) + "'")
        cmd ="curl -i --request POST \"http://194.210.120.41:8086/api/v2/write?org=InfluxDbCrowding&bucket=DetectionsDB&precision=s\"  --header \"Authorization: Token Kk2s4LBWEs_uQd3KiyVhMWsOmijSv16S3p8xZOGMTti5FnQCO4YTNS-UfCzAeUoPJNb2c5vTg6DEQ7tvkCdveg==\"  --header \"Content-Type: text/plain; charset=utf-8\"  --header \"Accept: application/json\" --data-binary 'medianstayngtime,device=" + deviceName + ",ipaddress=" + ipAddress + ",tecnology='wifi',type_data='no_randoms' medianstayngtime=" + str(0) + " " + str(int((dataAtual - dt.datetime(1970, 1, 1)).total_seconds())) + "'"
        os.system(cmd)


    cwifi.execute('select sum( (JulianDay(Last_Time_Found) - JulianDay(First_Record))  * 24 * 60   ) from Cellphone_Records_15 where (First_Record >= ? and First_Record <= ?) or (Last_Time_Found > ? and Last_Time_Found <= ?) and (ID LIKE "_2%" or ID LIKE "_6%" or ID LIKE "_A%" or ID LIKE "_E%"  ) ',(dataAnalizar, dataAtual, dataAnalizar, dataAtual))
    rows_tpm_only_randoms = cwifi.fetchall();
    if (rows_tpm_only_randoms[0][0] != None):
        #print("curl -i -XPOST \"https://sniff.iscte.me/write?db=mydb&precision=s\" --data-binary 'medianstayngtime,device=" + deviceName + ",tecnology='wifi',type_data='only_randoms' medianstayngtime=" + str(rows_tpm_only_randoms[0][0] / rows_only_randoms[0][0]) + " " + str(int((dataAnalizar - dt.datetime(1970, 1, 1)).total_seconds())) + "'")
        cmd ="curl -i --request POST \"http://194.210.120.41:8086/api/v2/write?org=InfluxDbCrowding&bucket=DetectionsDB&precision=s\"  --header \"Authorization: Token Kk2s4LBWEs_uQd3KiyVhMWsOmijSv16S3p8xZOGMTti5FnQCO4YTNS-UfCzAeUoPJNb2c5vTg6DEQ7tvkCdveg==\"  --header \"Content-Type: text/plain; charset=utf-8\"  --header \"Accept: application/json\" --data-binary 'medianstayngtime,device=" + deviceName + ",ipaddress=" + ipAddress + ",tecnology='wifi',type_data='only_randoms' medianstayngtime=" + str(float(rows_tpm_only_randoms[0][0]) / float(rows_only_randoms[0][0])) + " " + str(int((dataAtual - dt.datetime(1970, 1, 1)).total_seconds())) + "'"
        os.system(cmd)

    else:
        #print("curl -i -XPOST \"https://sniff.iscte.me/write?db=mydb&precision=s\" --data-binary 'medianstayngtime,device=" + deviceName + ",tecnology='wifi',type_data='only_randoms' medianstayngtime=" + str(0) + " " + str(int((dataAnalizar - dt.datetime(1970, 1, 1)).total_seconds())) + "'")
        cmd="curl -i --request POST \"http://194.210.120.41:8086/api/v2/write?org=InfluxDbCrowding&bucket=DetectionsDB&precision=s\"  --header \"Authorization: Token Kk2s4LBWEs_uQd3KiyVhMWsOmijSv16S3p8xZOGMTti5FnQCO4YTNS-UfCzAeUoPJNb2c5vTg6DEQ7tvkCdveg==\"  --header \"Content-Type: text/plain; charset=utf-8\"  --header \"Accept: application/json\" --data-binary 'medianstayngtime,device=" + deviceName + ",ipaddress=" + ipAddress + ",tecnology='wifi',type_data='only_randoms' medianstayngtime=" + str(0) + " " + str(int((dataAtual - dt.datetime(1970, 1, 1)).total_seconds())) + "'"
        os.system(cmd)
    """

# Dados Bluetooth

if(bluetoothBol==1) :

    connbluetooth = sqlite3.connect('/home/kali/Desktop/DB/project.db', timeout=30)
    cbluetooth = connbluetooth.cursor();

    # instante timinng

    cbluetooth.execute('select count(*) from Cellphone_Records where (First_Record >= ? and First_Record <= ?) or (Last_Time_Found > ? and Last_Time_Found <= ?)' , (dataAnalizar, dataAtual, dataAnalizar, dataAtual))
    rows = cbluetooth.fetchall();
    #print(rows)

    cbluetooth.execute('select count(*) from Cellphone_Records where ((First_Record >= ? and First_Record <= ?) or (Last_Time_Found > ? and Last_Time_Found <= ?)) and ID NOT LIKE "_2%" and ID NOT LIKE "_6%" and ID NOT LIKE "_A%" and ID NOT LIKE "_E%"  ' , (dataAnalizar, dataAtual, dataAnalizar, dataAtual))
    rows_no_randoms = cbluetooth.fetchall();

    cbluetooth.execute('select count(*) from Cellphone_Records where ((First_Record >= ? and First_Record <= ?) or (Last_Time_Found > ? and Last_Time_Found <= ?)) and (ID LIKE "_2%" or ID LIKE "_6%" or ID LIKE "_A%" or ID LIKE "_E%"  )',(dataAnalizar, dataAtual, dataAnalizar, dataAtual))
    rows_only_randoms = cbluetooth.fetchall();
    

    # Envio para o InfluxDb

    #print("curl -i   --request POST \"http://194.210.120.41:8086/api/v2/write?org=TomasWorkspace&bucket=DetectionsDB&precision=s\"  --header \"Authorization: Token PnyTV3BaonLB7-pTpKsuvUySrPLRn12OnORqIHwby3HVJiaUxy9XSqI1ByitibVaan9wNXxdaLZvh8ECp5WU5w==\"  --header \"Content-Type: text/plain; charset=utf-8\"  --header \"Accept: application/json\" --data-binary 'numdetectionstable,device="+ deviceName + ",tecnology='bluetooth',type_data='all' numdetections=" + str(rows[0][0]) + " " + str(int( (dataAtual - dt.datetime(1970,1,1)).total_seconds())) + "'")
    cmd="curl -i   --request POST \"http://194.210.120.41:8086/api/v2/write?org=TomasWorkspace&bucket=DetectionsDB&precision=s\"  --header \"Authorization: Token PnyTV3BaonLB7-pTpKsuvUySrPLRn12OnORqIHwby3HVJiaUxy9XSqI1ByitibVaan9wNXxdaLZvh8ECp5WU5w==\"  --header \"Content-Type: text/plain; charset=utf-8\"  --header \"Accept: application/json\" --data-binary 'numdetectionstable,device="+ deviceName + ",tecnology='bluetooth',type_data='all' numdetections=" + str(rows[0][0]) + " " + str(int( (dataAtual - dt.datetime(1970,1,1)).total_seconds())) + "'"
    os.system(cmd)

    #print("curl -i   --request POST \"http://194.210.120.41:8086/api/v2/write?org=TomasWorkspace&bucket=DetectionsDB&precision=s\"  --header \"Authorization: Token PnyTV3BaonLB7-pTpKsuvUySrPLRn12OnORqIHwby3HVJiaUxy9XSqI1ByitibVaan9wNXxdaLZvh8ECp5WU5w==\"  --header \"Content-Type: text/plain; charset=utf-8\"  --header \"Accept: application/json\" --data-binary 'numdetectionstable,device="+ deviceName + ",tecnology='bluetooth',type_data='no_randoms' numdetections=" + str(rows_no_randoms[0][0]) + " " + str(int( (dataAtual - dt.datetime(1970,1,1)).total_seconds())) + "'")
    cmd="curl -i   --request POST \"http://194.210.120.41:8086/api/v2/write?org=TomasWorkspace&bucket=DetectionsDB&precision=s\"  --header \"Authorization: Token PnyTV3BaonLB7-pTpKsuvUySrPLRn12OnORqIHwby3HVJiaUxy9XSqI1ByitibVaan9wNXxdaLZvh8ECp5WU5w==\"  --header \"Content-Type: text/plain; charset=utf-8\"  --header \"Accept: application/json\" --data-binary 'numdetectionstable,device="+ deviceName + ",tecnology='bluetooth',type_data='no_randoms' numdetections=" + str(rows_no_randoms[0][0]) + " " + str(int( (dataAtual - dt.datetime(1970,1,1)).total_seconds())) + "'"
    os.system(cmd)

    #print("curl -i   --request POST \"http://194.210.120.41:8086/api/v2/write?org=TomasWorkspace&bucket=DetectionsDB&precision=s\"  --header \"Authorization: Token PnyTV3BaonLB7-pTpKsuvUySrPLRn12OnORqIHwby3HVJiaUxy9XSqI1ByitibVaan9wNXxdaLZvh8ECp5WU5w==\"  --header \"Content-Type: text/plain; charset=utf-8\"  --header \"Accept: application/json\" --data-binary 'numdetectionstable,device="+ deviceName + ",tecnology='bluetooth',type_data='only_randoms' numdetections=" + str(rows_only_randoms[0][0]) + " " + str(int( (dataAtual - dt.datetime(1970,1,1)).total_seconds())) + "'")
    cmd="curl -i   --request POST \"http://194.210.120.41:8086/api/v2/write?org=TomasWorkspace&bucket=DetectionsDB&precision=s\"  --header \"Authorization: Token PnyTV3BaonLB7-pTpKsuvUySrPLRn12OnORqIHwby3HVJiaUxy9XSqI1ByitibVaan9wNXxdaLZvh8ECp5WU5w==\"  --header \"Content-Type: text/plain; charset=utf-8\"  --header \"Accept: application/json\" --data-binary 'numdetectionstable,device="+ deviceName + ",tecnology='bluetooth',type_data='only_randoms' numdetections=" + str(rows_only_randoms[0][0]) + " " + str(int( (dataAtual - dt.datetime(1970,1,1)).total_seconds())) + "'"
    os.system(cmd)
 
    

# Temperatura do CPU
if( cpuTempBol == 1):
    cmd ="curl -i --request POST \"http://194.210.120.41:8086/api/v2/write?org=TomasWorkspace&bucket=CPUTemperatures&precision=s\"  --header \"Authorization: Token PnyTV3BaonLB7-pTpKsuvUySrPLRn12OnORqIHwby3HVJiaUxy9XSqI1ByitibVaan9wNXxdaLZvh8ECp5WU5w==\"  --header \"Content-Type: text/plain; charset=utf-8\"  --header \"Accept: application/json\" --data-binary 'cpuTemperature,device="+ deviceName + " cpuTemperature=" + str(cpuTemp) + " " + str(int( (dataAtual - dt.datetime(1970,1,1)).total_seconds())) + "'"
    os.system(cmd)    
        
        
