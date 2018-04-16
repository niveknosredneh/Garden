#!/bin/bash

#backup 1 at a time past limit
lines=$( cat humidity.txt | wc -l )
if [ $lines > 500 ]
then 
	head humidity.txt -n 1 >> humidity.txtbk; 
	tail humidity.txt -n +2 > humidity.tmp;
	mv humidity.tmp humidity.txt;
fi
lines=$( cat temp.txt | wc -l )
if [ $lines > 500 ]
then 
	head temp.txt -n 1 >> temp.txtbk;
	tail temp.txt -n +2 > temp.tmp;
	mv temp.tmp temp.txt;
fi
lines=$( cat tempD.txt | wc -l )
if [ $lines > 500 ]
then 
	head tempD.txt -n 1 >> tempD.txtbk;
	tail tempD.txt -n +2 > tempD.tmp;
	mv tempD.tmp tempD.txt;
fi
lines=$( cat soil.txt | wc -l )
if [ $lines > 500 ]
then 
	head soil.txt -n 1 >> soil.txtbk;
	tail soil.txt -n +2 > soil.tmp;
	mv soil.tmp soil.txt;
fi


# run until success 
until /usr/bin/python ~/LightSensor/PythonSerial.py; do
	sleep 1    
done

