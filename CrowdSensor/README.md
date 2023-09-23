# Crowd Sensor

This directory contains the source code of the STToolkit's sensors.

## aircrack-ng-1.7

This directory contains a costumized version of the aircrack-ng software suite. It purposefully costumized for the STToolkit. This aircrack-ng version was costumized based on the latest aircrack-ng 1.7 original version available at the [Aircrack-ng main page](https://www.aircrack-ng.org/). 

The crowd sensors make the use of two applications of aircrack-ng: `airmon-ng` and `airodump-ng`. The `airmon-ng` is used to entable the monitor mode of a wireless interface, and the `airodump-ng` is used to capture raw Wi-Fi packets from mobile devices. The latter was the only application that was purposefully costumized for performing the device counting and inserting the collected data into the _DeviceRecords.db_ database, the sensor's local database. The remaining applications are not relevant for the STToolkit.

