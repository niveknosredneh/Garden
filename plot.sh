#!/bin/bash

#backup 1 at a time past limit
lines=$( cat humidity.txt | wc -l )

if [ $lines > 500 ]
then 
	head humidity.txt -n 1 >> humidity.txtbk; 
	tail humidity.txt -n +2 > humidity.tmp;
	mv humidity.tmp humidity.txt;
fi
lines=$( cat tempA.txt | wc -l )
if [ $lines > 500 ]
then 
	head tempA.txt -n 1 >> tempA.txtbk;
	tail tempA.txt -n +2 > tempA.tmp;
	mv tempA.tmp tempA.txt;
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

