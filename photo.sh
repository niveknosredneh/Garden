#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M")

raspistill --annotate 12 -rot 270 -w 3280 -h 2464 -o /home/kevin/LightSensor/garden.jpg
