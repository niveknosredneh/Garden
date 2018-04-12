#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
PythonSerial.py

Reads serial data from arduino and logs the data while also outputing new graphs


Kevin Henderson 2018

"""

import serial
from datetime import datetime, date, time

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

import matplotlib.pyplot as plt

# make graphs more like matlab
plt.style.use('ggplot') # thanks Juris!

import matplotlib.dates as mdates
from matplotlib.dates import strpdate2num, num2date

import numpy as np


"""Open the serial port"""
# fix so USB0 or USB1 can be used so as to not fail
# open arduino serial object
try:
    arduino = serial.Serial("/dev/ttyUSB0",timeout=5,baudrate=9600)
except:
    print('Please check the port')


rawdata = ''
dt = datetime.now() # get current time

"""Receiving data """
# 2 floats should be 8 chars, if less then serial receive failed
while ( len(rawdata.strip()) < 6):
    rawdata = str(arduino.readline()) # read input from arduino
    print rawdata.strip()

""" writing data to file """
def write(L):
    print "writing to file...\n"
	
    light,temp,soil,humidity,tempD = rawdata.split(";") # splits rawdata into proper data values 

    file=open("/home/kevin/LightSensor/light.txt",mode='aw')
    file.write(dt.strftime("%Y%m%d%H%M%S") +"  " + light + "\n")
    file.close()

    file=open("/home/kevin/LightSensor/temp.txt",mode='aw')
    file.write(dt.strftime("%Y%m%d%H%M%S") +"  " + temp+ "\n")
    file.close()

    file=open("/home/kevin/LightSensor/soil.txt",mode='aw')
    file.write(dt.strftime("%Y%m%d%H%M%S") +"  " + soil+ "\n") 
    file.close()

    file=open("/home/kevin/LightSensor/humidity.txt",mode='aw')
    file.write(dt.strftime("%Y%m%d%H%M%S") +"  " + humidity+ "\n")
    file.close()

    file=open("/home/kevin/LightSensor/tempD.txt",mode='aw')
    file.write(dt.strftime("%Y%m%d%H%M%S") +"  " + tempD) # automatically adds \n
    file.close()

write(rawdata) # see above

""" Begin plotting """

print "plotting Light graph"
dates1,lightData = np.genfromtxt("/home/kevin/LightSensor/light.txt", unpack=True,
        converters={ 0: mdates.strpdate2num('%Y%m%d%H%M%S')})

fig, ax = plt.subplots()
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
plt.gcf().autofmt_xdate()
plt.plot_date(x=dates1, y=lightData, fmt="y-")
plt.title("Light Intensity")
plt.ylabel("Light %")
plt.savefig('/home/kevin/LightSensor/light.png')
plt.close()

print "plotting Temperature graph" # to plots on 1 graph
dates2,tempData = np.genfromtxt("/home/kevin/LightSensor/temp.txt", unpack=True,
        converters={ 0: mdates.strpdate2num('%Y%m%d%H%M%S')})
dates3,tempDigitalData = np.genfromtxt("/home/kevin/LightSensor/tempD.txt", unpack=True,
        converters={ 0: mdates.strpdate2num('%Y%m%d%H%M%S')})

fig, ax = plt.subplots()
line1, = plt.plot_date(x=dates2, y=tempData, label="Analog Sensor", fmt="r-")
line2, = plt.plot_date(x=dates2, y=tempDigitalData, label="Digital Sensor", fmt="m-")
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
plt.gcf().autofmt_xdate()
plt.legend([line1, line2], ["Analog Sensor", "Digital Sensor"], loc=2) # label top left
plt.title("Temperature")
plt.ylabel("Degrees Celsius")
plt.savefig('/home/kevin/LightSensor/temp.png')
plt.close()

print "plotting Moisture graph"
dates4,soilData = np.genfromtxt("/home/kevin/LightSensor/soil.txt", unpack=True,
        converters={ 0: mdates.strpdate2num('%Y%m%d%H%M%S')})

fig, ax = plt.subplots()
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
plt.gcf().autofmt_xdate()
plt.plot_date(x=dates4, y=soilData, fmt="b-")
plt.title("Substrate Aridity (Moisture)")
plt.ylabel("Completely Submerged = 200   /   Bone Dry = 1000")
plt.savefig('/home/kevin/LightSensor/soil.png')
plt.close()

print "plotting Humidity graph"
dates5,soilData = np.genfromtxt("/home/kevin/LightSensor/humidity.txt", unpack=True,
        converters={ 0: mdates.strpdate2num('%Y%m%d%H%M%S')})

fig, ax = plt.subplots()
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
plt.gcf().autofmt_xdate()
plt.plot_date(x=dates5, y=soilData, fmt="c-")
plt.title("Relative Humidity")
plt.ylabel("Humidity %")
plt.savefig('/home/kevin/LightSensor/humidity.png')
plt.close()



