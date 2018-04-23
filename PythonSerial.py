#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
PythonSerial.py

Reads serial data from arduino and logs the data while also outputing new graphs


Kevin Henderson 2018

"""

USE_SERIAL = False # 0 for esp8266, 1 for usb serial

import serial
import urllib2
from datetime import datetime, date, time

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

import matplotlib.pyplot as plt

# make graphs more like matlab
plt.style.use('ggplot') # thanks Juris!

import matplotlib.dates as mdates
from matplotlib.dates import strpdate2num, num2date

import matplotlib.ticker as mtick

import numpy as np


# Open the serial port
# fix so USB0 or USB1 can be used so as to not fail
# open arduino serial object
if(USE_SERIAL):
	try:
		arduino = serial.Serial("/dev/ttyUSB0",timeout=5,baudrate=9600)
	except( nameError ):
		print('No serial connection found on /dev/ttyUSB0')
		pass
	try:
		arduino = serial.Serial("/dev/ttyUSB1",timeout=5,baudrate=9600)
	except( nameError ):
		print('No serial connection found on /dev/ttyUSB1')
		pass
	try:
		arduino = serial.Serial("/dev/ttyACM0",timeout=5,baudrate=9600)
	except( nameError ):
		print('No serial connection found on /dev/ttyACM0')
	

rawdata = ''
dt = datetime.now() # get current time

dataList = [6,8] # just placeholders

data = urllib2.urlopen("http://192.168.100.104/")

"""Receiving data """
# should give 8 results, dont want DHT init output
while ( len(rawdata.strip()) < 30 or len(rawdata.strip()) > 35):
    if(USE_SERIAL):
        rawdata = str(arduino.readline()) # read input from arduino
    else:
        rawdata = str(data.readline()) # read input from Wifi
        print rawdata

""" writing data to file """
def write(L):
    try:
        temp,soil,humidity,tempD,humidity2,tempD2 = rawdata.split(";") # splits rawdata into proper data values 
    except ValueError:
        print("was expecting different number of values!")

    print "writing tempA.txt" 
    file=open("/home/kevin/LightSensor/tempA.txt",mode='aw')
    file.write(dt.strftime("%Y%m%d%H%M%S") +"  " + temp+ "\n")
    file.close()

    print "writing soil.txt" 
    file=open("/home/kevin/LightSensor/soil.txt",mode='aw')
    file.write(dt.strftime("%Y%m%d%H%M%S") +"  " + soil+ "\n") 
    file.close()

    print "writing humidity.txt" 
    file=open("/home/kevin/LightSensor/humidity.txt",mode='aw')
    file.write(dt.strftime("%Y%m%d%H%M%S") +"  " + humidity+ "\n")
    file.close()

    print "writing tempD.txt" 
    file=open("/home/kevin/LightSensor/tempD.txt",mode='aw')
    file.write(dt.strftime("%Y%m%d%H%M%S") +"  " + tempD+ "\n") 
    file.close()

    print "writing humidity2.txt" 
    file=open("/home/kevin/LightSensor/humidity2.txt",mode='aw')
    file.write(dt.strftime("%Y%m%d%H%M%S") +"  " + humidity2+ "\n")
    file.close()

    print "writing tempD2.txt" 
    file=open("/home/kevin/LightSensor/tempD2.txt",mode='aw')
    file.write(dt.strftime("%Y%m%d%H%M%S") +"  " + tempD2)
    file.close()



write(rawdata) # see above

""" Begin plotting """

print "plotting Temperature graph" # to plots on 1 graph
dates2,tempData = np.genfromtxt("/home/kevin/LightSensor/tempA.txt", unpack=True,
        converters={ 0: mdates.strpdate2num('%Y%m%d%H%M%S')})
dates3,tempDigitalData = np.genfromtxt("/home/kevin/LightSensor/tempD.txt", unpack=True,
        converters={ 0: mdates.strpdate2num('%Y%m%d%H%M%S')})
dates31,tempDigitalData2 = np.genfromtxt("/home/kevin/LightSensor/tempD2.txt", unpack=True,
        converters={ 0: mdates.strpdate2num('%Y%m%d%H%M%S')})

#average of two
avgTemp = np.add(tempData,tempDigitalData)
avgTemp /= 2.0

fig, ax = plt.subplots()

line3, = plt.plot_date(x=dates31, y=tempDigitalData2, label="Digital Sensor ambient", fmt="y-",linewidth=3.0)
line1, = plt.plot_date(x=dates2, y=tempData, label="Analog Sensor probe", fmt="r.")
line2, = plt.plot_date(x=dates3, y=tempDigitalData, label="Digital Sensor probe", fmt="m.")
line12, = plt.plot_date(x=dates2, y=avgTemp, label="Average", fmt="k-",linewidth=2.0)

ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
plt.gcf().autofmt_xdate()

# sets up legend
legend = plt.legend([line3, line1, line2, line12], ["Ambient", "Probe Analog", "Probe Digital", "Probe Average"], loc="best")
frame = legend.get_frame()
frame.set_facecolor('white')

# adds celcius to axis
type(ax)
vals = ax.get_yticks()
ax.set_yticklabels(['{:3.1f}$^\circ$C'.format(x*1) for x in vals])

plt.title("Temperature")
plt.savefig('/home/kevin/LightSensor/temp.png')
plt.close()

print "plotting Moisture graph"
dates4,soilData = np.genfromtxt("/home/kevin/LightSensor/soil.txt", unpack=True,
        converters={ 0: mdates.strpdate2num('%Y%m%d%H%M%S')})

soilData /= 10.0 # to get into percent roughly. 0.0% to 102.3%  

fig, ax = plt.subplots()
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))

plt.gcf().autofmt_xdate()
plt.plot_date(x=dates4, y=soilData, fmt="b-")
plt.title("Substrate Moisture")

# adds % to axis
type(ax)
vals = ax.get_yticks()
ax.set_yticklabels(['{:3.1f}%'.format(x*1) for x in vals])

#plt.ylabel("Percent Saturated")
plt.savefig('/home/kevin/LightSensor/soil.png')
plt.close()

print "plotting Humidity graph"
dates5,humidityData = np.genfromtxt("/home/kevin/LightSensor/humidity.txt", unpack=True,
        converters={ 0: mdates.strpdate2num('%Y%m%d%H%M%S')})
dates6,humidityData2 = np.genfromtxt("/home/kevin/LightSensor/humidity2.txt", unpack=True,
        converters={ 0: mdates.strpdate2num('%Y%m%d%H%M%S')})

fig, ax = plt.subplots()
line1, = plt.plot_date(x=dates5, y=humidityData, label="probe", fmt="c-")
line2, = plt.plot_date(x=dates6, y=humidityData2, label="ambient", fmt="b-")

ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
plt.gcf().autofmt_xdate()

# sets up legend
legend = plt.legend([line1, line2], ["Probe", "Ambient"], loc="best")
frame = legend.get_frame()
frame.set_facecolor('white')

# adds % to axis
type(ax)
# manipulate
vals = ax.get_yticks()
ax.set_yticklabels(['{:3.1f}%'.format(x*1) for x in vals])

plt.title("Relative Humidity")
plt.savefig('/home/kevin/LightSensor/humidity.png')
plt.close()

print "Success!"



