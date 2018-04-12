/*
 * Kevin Henderson 2018
 * 

Garden setup

*/

#include <Arduino.h>
#include <Wire.h>
#include <DHT.h>

#define DHTPIN 5     // what digital pin we're connected to
#define DHTTYPE DHT11   // DHT 11

int photoPin = A0;    // photresistor
int tempPin = A7;     //  TMP36 sensor
int soilApin = A4;    // LM393 analog moisture sensor


float tempValue = 0;
float temperature = 0;
float lightValue = 0;  // variable to store the value coming from the sensor
float lightPercent = 0;

float humidity = 0;
float temperatureDigital = 0;
int soilAnalog = 0;

DHT dht(5,DHT11);

void setup() {
   
  pinMode(photoPin, INPUT);
  pinMode(tempPin, INPUT);
  pinMode(soilApin, INPUT);
  pinMode(5, INPUT);

  
  Serial.begin(9600); // trying higher baud
}

void loop() {
  
  lightValue = analogRead(photoPin);
  lightPercent = (lightValue / 1023) * 100;
  
  tempValue = analogRead(tempPin);

  soilAnalog = analogRead(soilApin);

  humidity = dht.readHumidity();
  temperatureDigital = dht.readTemperature();

  // Check if any reads failed and exit early (to try again).
  if (isnan(humidity) || isnan(temperatureDigital)) {
    Serial.println("Failed to read from DHT sensor");
  return;
  }
  

   //Voltage at pin in milliVolts = (reading from ADC) * (5000/1024)
  float tempVoltage = tempValue * 0.004882814;
  //Centigrade temperature = [(analog voltage in mV) - 500] / 10
  temperature = (tempVoltage - 0.5) * 100.0;

  Serial.println((String)lightPercent+';'+(String)temperature
            +';'+(String)soilAnalog+';'+(String)humidity				    +';'+(String)temperatureDigital);


  Serial.flush();

  delay(3000);
}
