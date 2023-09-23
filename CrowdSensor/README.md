# Crowd Sensor

This directory contains the source code of the STToolkit's crowd sensors.

## aircrack-ng-1.7

This directory contains a costumized version of the aircrack-ng software suite. It purposefully costumized for the STToolkit. This aircrack-ng version was costumized based on the latest aircrack-ng 1.7 original version available at the [Aircrack-ng main page](https://www.aircrack-ng.org/).

The crowd sensors make the use of two applications of aircrack-ng: `airmon-ng` and `airodump-ng`. The `airmon-ng` is used to enable the monitor mode of the wireless detection interface, and the `airodump-ng` is used to capture raw Wi-Fi packets from mobile devices. The latter is the only application that was purposefully costumized from the original version.

## DB

This directory contains a `DeviceRecords.db` file. This file is the sensor's local database, where the collected data from the sensor will be stored.












