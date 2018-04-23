#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M")

# takes picture and updates old
raspistill -rot 270 -w 3280 -h 2464 -o ~/LightSensor/screenshots/garden.jpg

# copies new picture to home folder with current date as filename
# to be used to capture timelapses
cp ~/LightSensor/screenshots/garden.jpg ~/$DATE.jpg

# resizes and annotes date in preperation for gif
convert ~/$DATE.jpg -resize 480x320 -pointsize 32 -fill white -annotate +25+310 %[exif:DateTimeOriginal] ~/resized/$DATE.jpg

cd ~/resized/
NUMFILES=$(ls -l | wc -l)
if [ $NUMFILES > 24 ]
then
	ls | head -n -24 | xargs rm -rf
fi

# makes animated gif from all files in resized directory
convert -delay 20 -loop 0 ~/resized/*.jpg ~/LightSensor/screenshots/myimage.gif
