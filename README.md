# Kevin's Garden Automation and Datalogging

<img src="https://github.com/niveknosredneh/Garden/blob/master/screenshots/temp.png" width="640" align="middle">

Analog/Digital sensors hooked up to Arduino/Atmega328P, processing data and sending via USB/Serial or ESP8266/Wifi to a Raspberry Pi.

The Pi logs the data and creates a new graph with python and the matplotlib library.
A cron job can be set to automate this on a regular interval while also running a script to capture a current photo.

The Pi can also runs the lighttpd web server, hosting this data on the world wide web.

While anyone looking to run this likely won't be using all the sensors, it should be easy to modify the code the suits your needs.


TODO:
- ~~add humidity sensing capabilities with the DHT11 sensor~~
- ~~remove required USB cable by using the ESP8266 module~~
- add 5V relay with water pump to enable automatic watering 
- ~~create backup script to only show ~72 hours worth of data~~


## Prerequisites

### Software
- Python 2.7.x
- Matplotlib/Pyplot/Numpy python libraries
- [Pyserial](https://github.com/pyserial/pyserial) - if connecting to Pi through USB
- [Adafruit_Sensor](https://github.com/adafruit/Adafruit_Sensor) and [DHT-sensor-library](https://github.com/adafruit/DHT-sensor-library) placed into your library folder
- [ESP8266 Arduino library](https://github.com/esp8266/Arduino) - if using ESP8266 module for Wifi
- (Optionally) run [PlatformIO](https://platformio.org/) on the Pi for headless updating of the arduino over ssh

### Hardware
- Arduino Uno or Nano
- TMP36 temperature sensor
- ~~Photoresistor~~ (removed for now) 
- ~~10K resistor~~
- Analog moisture sensor
- DHT11 digital temperature and humidity sensor
- ESP8266 wifi module for wireless communication with Pi

<img src="https://github.com/niveknosredneh/Garden/blob/master/screenshots/Circuit.png" width="640" align="middle">

## Running

main.cpp in ./src is to be compiled and uploaded to the Arduino.

ESP8266main.cpp in ./src is to be compiled and uploaded to the ESP8266. (Hint: use the serial from Arduino w/ blank sketch)

plot.sh is meant to run as a cron job as it continuously runs the python script until it succeeds. Also serves as backup script checking for the number of data points and backing up 1 by 1 if over X amount. 

PythonSerial.py can be run standalone but my shoddy serial connection makes using plot.sh much easier.  Edit flag in py file for either serial or Wifi use.

Confirmed working on:

Raspberry Pi 1-B w/ Raspbian 8 (Jessie)- Arduino Nano w/ Atmega328 - Python 2.7.9 - Matplotlib 1.4.2

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Juris for helping me beautify my graphs
