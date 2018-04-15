/*
 * Kevin Henderson 2018
 * 

Garden setup
Sensors sending serial data to be logged
temperature, humidity, light and soil moisture

*/

#include <Arduino.h>
#include <DHT.h> // requires adafruit_sensor library

#include <SoftwareSerial.h>
SoftwareSerial ESPserial(2, 3); // RX | TX


int ledPin = 10;
// int photoPin = A0;    // photresistor
int tempPin = A7;     //  TMP36 sensor
int soilApin = A4;    // LM393 analog moisture sensor
int dhtPin = 5;     // DHT11 digital humidity/temperature

DHT dht(dhtPin,DHT11); // running DHT11, change for DHT22 or other

void setup() {
   
//  pinMode(photoPin, INPUT);
  pinMode(tempPin, INPUT);
  pinMode(soilApin, INPUT);
  pinMode(dhtPin, INPUT);
  pinMode(ledPin, OUTPUT);


    // Start the software serial for communication with the ESP8266
    ESPserial.begin(9600);  
}

void loop() {

   
  // Light
//  int lightValue = analogRead(photoPin);
//  float lightPercent = (lightValue / 1023) * 100; // Analog pins have 1023 steps

  // Temperature
  int tempValue = analogRead(tempPin);
  //Voltage at pin in milliVolts = (reading from ADC) * (5000/1024)
  float tempVoltage = tempValue * 0.004882814;
  //Centigrade temperature = [(analog voltage in mV) - 500] / 10
  float temperature = (tempVoltage - 0.5) * 100.0;

  // Soil Moisture
  int soilAnalog = analogRead(soilApin);
  int moisture = 0;

  // doing this makes more moisture higher value instead of lower value
  // makes more sense from visual/graphical standpoint
  if(soilAnalog>512) { moisture = soilAnalog -  (2 * (soilAnalog - 512) ); }
  else if(soilAnalog<512) { moisture = soilAnalog +  (2 * (512- soilAnalog) ); }


  // Humidity
  float humidity = dht.readHumidity();
  float temperatureDigital = dht.readTemperature();
  // Check if any reads failed on DHT11 and exit early (to try again).
  if (isnan(humidity) || isnan(temperatureDigital)) {
    ESPserial.println("Failed to read from DHT sensor");
    //analogWrite(ledPin, 0);
  return;
  }

  // print to serial in order: 1-light 2-analogTemp 3-moisture 4-humidity 5-digitalTemp
   if (ESPserial.available()) { 
      ESPserial.println(
   //    (String)lightPercent+';'+
      (String)temperature+';'+(String)moisture
       +';'+(String)humidity+';'+(String)temperatureDigital);
   }
  
  ESPserial.flush();

  int i = 768;
  while(i>512) { analogWrite(ledPin, i); i--; delay(5); }
  
  delay(3000);
}
