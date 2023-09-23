# Crowd Sensor

This directory contains the source code of the STToolkit's crowd sensors.

This is a project for Linux systems only. You also will need to have a Wi-Fi dongle that supports monitor mode to capture device messages in the sensors vicinity. You can find a list of Wi-Fi cards that support monitor mode [here](https://www.aircrack-ng.org/doku.php?id=faq#what_is_the_best_wireless_card_to_buy).


## Getting Started

Fisrt, download the full `CrowdSensor` repository and insert it on the `/Desktop` directory of your Linux device.

### Install Aircrack-ng customized version

The `aircrack-ng-1.7` is a costumized software suite that was purposefully customized for the STToolkit for detecting Wi-Fi devices in the sensor's proximity.

Install the building requirements from [here](https://github.com/aircrack-ng/aircrack-ng/blob/master/README.md#requirements).

Install the dependencies from [here](https://github.com/aircrack-ng/aircrack-ng/blob/master/README.md#linux).

 To build `aircrack-ng`, run the following commands:
```
cd aircrack-ng-1.7
autoreconf -i
./configure 
make
make test
make install
ldconfig
```

### Configure a InfluxDB Upload configuration

Run the `influxDBUploadConfig.py` python script.

```
python3 influxDBUploadConfig.py
```

Insert the Cloud Server IP Address, InfluxDB Organization name, InfluxDB Bucket, and the InfluxDB Atuthorization token.

Check the InfluxDB Upload configuration by running the `checkInfluxDBConfig.py` python script.

```
python3 checkInfluxDBConfig.py
```

### Set the sensor deployment location

Run the `sendSensorLocation.py` python script.

```
python3 sendSensorLocation.py
```

Insert the sensor name.

**_NOTE:_**  Do not insert spaces in the sensor name. For spaces, use "_" instead. (E.g.: Public\_Entrance)

Insert the latitude and longitude coordinates, where the sensor is/will be deployed. 

**_NOTE:_**  The latitude and longitude needs to be inserted individually. You can get the these values using [Google Maps](https://www.google.com/maps).

Confirm the values. If a 'HTTP 204 No Content' appears on the output, the sensor location was sent to the InfluxDB database. If this output does not appear, please check if the InfluxDB Upload configuration was set correctly.

**_NOTE:_** If you want to change the location of the sensor, simply run this script again, inserting the same sensor name.

### Tasks Automation configuration

Open 'crontab'.

```
crontab -u <your_user> -e
```

Select your prefereed text editor. It is on this file that you will configure the automation of tasks that the sensor needs to perform.

Replace the contents of the 'crontab' file to the ones on the 'crontab_tasks_automation.txt' file.

Go to the end of the file. Look for the lines that have "Uncomment" at the end of each line, and uncomment them (remove the # in the beginning of each line and also the "Uncomment" word).

The parameters that you can change for each task are highlighted in **bold**.

 * @reboot sudo airmon-ng start **wlan0**
     * wlan0 -> Raspberry Pi 4
     * wlan1 -> Raspberry Pi 3

* \*/10 \* \* \* \* timeout -k 1 590s sudo airodump-ng background 1 **wlan0**
     * wlan0 -> Raspberry Pi 4
     * wlan1 -> Raspberry Pi 3
 
* \*/5 \* \* \* \* /usr/bin/python3 /home/kali/Desktop/sendCrowdingData.py SensorTest Wifi 5 **wlan1**
    * wlan1 -> Raspberry Pi 4
    * wlan0 -> Raspberry Pi 3

Save the ´crontab' file.

The tasks automation of the sensor are now configured.

You can check the changes by printing the crontab file.

```
crontab -u <your_user> -l
```

You should see the crontab file with the sensor tasks automation.

















