#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M")

cd ~/LightSensor/

for i in *.png; 
do
	cp "$i" backup/$DATE"_$i";
done
