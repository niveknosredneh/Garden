#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

Kevin Henderson


"""

import serial
from datetime import datetime, date, time

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

import matplotlib.pyplot as plt
plt.style.use('ggplot') # thanks Juris!

import matplotlib.dates as mdates
from matplotlib.dates import strpdate2num, num2date

import numpy as np


"""Open the serial port"""
try:
    arduino = serial.Serial("/dev/ttyUSB0",timeout=1,baudrate=9600)
except:
    print('Please check the port')


rawdata = ''
dt = datetime.now()

"""Receiving data """
# 2 floats should be 8 chars, if less then serial receive failed
while len(rawdata.strip())<7:
    rawdata = str(arduino.readline())
print rawdata

""" writing data to file """
def write(L):
    print "writing to file...\n"
    light,temp,soil = rawdata.split(";")
    file=open("/home/kevin/LightSensor/light.txt",mode='aw')
    file.write(dt.strftime("%Y%m%d%H%M%S") +"  " + light + "\n")
    file.close()

    file=open("/home/kevin/LightSensor/temp.txt",mode='aw')
    file.write(dt.strftime("%Y%m%d%H%M%S") +"  " + temp+ "\n")
    file.close()

    file=open("/home/kevin/LightSensor/soil.txt",mode='aw')
    file.write(dt.strftime("%Y%m%d%H%M%S") +"  " + soil) # automatically adds \n
    file.close()

write(rawdata)

""" Begin plotting """

print "plotting Light graph"
dates1,lightData = np.genfromtxt("/home/kevin/LightSensor/light.txt", unpack=True,
        converters={ 0: mdates.strpdate2num('%Y%m%d%H%M%S')})

fig, ax = plt.subplots()
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
plt.gcf().autofmt_xdate()
plt.plot_date(x=dates1, y=lightData, fmt="r-")
plt.title("Light Intensity")
plt.ylabel("Light %")
plt.savefig('/home/kevin/LightSensor/light.png')
plt.close()

print "plotting Temperature graph"
dates2,tempData = np.genfromtxt("/home/kevin/LightSensor/temp.txt", unpack=True,
        converters={ 0: mdates.strpdate2num('%Y%m%d%H%M%S')})

fig, ax = plt.subplots()
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
plt.gcf().autofmt_xdate()
plt.plot_date(x=dates2, y=tempData, fmt="r-")
plt.title("Temperature")
plt.ylabel("Degrees Celsius")
plt.savefig('/home/kevin/LightSensor/temp.png')
plt.close()

print "plotting Moisture graph"
dates2,soilData = np.genfromtxt("/home/kevin/LightSensor/soil.txt", unpack=True,
        converters={ 0: mdates.strpdate2num('%Y%m%d%H%M%S')})

fig, ax = plt.subplots()
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
plt.gcf().autofmt_xdate()
plt.plot_date(x=dates2, y=soilData, fmt="r-")
plt.title("Substrate Aridity (Moisture)")
plt.ylabel("Completely Submerged = 200   /   Bone Dry = 1000")
plt.savefig('/home/kevin/LightSensor/soil.png')
plt.close()



