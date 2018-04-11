#!/bin/bash

# run until success 
until /usr/bin/python /home/kevin/LightSensor/PythonSerial.py; do
	sleep 2    
done
