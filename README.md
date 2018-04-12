<img src="https://github.com/niveknosredneh/Garden/blob/master/screenshots/temp.png" width="420" align="left">
<img src="https://github.com/niveknosredneh/Garden/blob/master/screenshots/Circuit.png" width="480" align="right">

# Kevin's Garden Automation and Datalogging

Analog sensors hooked up to Arduino/Atmega328P, processeing data and sending via serial connection over USB to a Raspberry Pi.

The Pi logs the data and creates a new graph with python and the matplotlib library.
A cron job can be set to automate this on a regular interval while also running a script to capture a current photo.

The Pi can also runs the lighttpd web server, hosting this data on the world wide web.

TODO:
- add humidity sensing capabilities with the DHT11 sensor 
- add relay with water pump to enable automatic watering 
- create backup script to only show 72 hours worth of data

## Prerequisites

- python 2.7.x
- matplotlib/pyplot
- https://github.com/pyserial/pyserial

- TMP36 temperature sensor
- Photoresistor
- LM393 driven analog moisture sensor


## Running

LightSensor.ino is the Arduino sketch which must be uploaded to your board

plot.sh is meant to run as a cron job as it continuously runs the python script until it succeeds.

PythonSerial.py can be run standalone but my shoddy serial connection makes using plot.sh much easier.

Confirmed working on:

-Python 2.7.9

-Matplotlib 1.4.2

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Juris for helping me beautify my graphs
