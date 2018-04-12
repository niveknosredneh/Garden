/*
 * Kevin Henderson 2018
 * 

Garden setup

*/

int photoPin = A0;    // photresistor
int tempPin = A7;     //  TMP36 sensor
int soilApin = A4;    // LM393 analog moisture sensor


float tempValue = 0;
float temperature = 0;
float lightValue = 0;  // variable to store the value coming from the sensor
float lightPercent = 0;

int soilAnalog = 0;

void setup() {
   
  pinMode(photoPin, INPUT);
  pinMode(tempPin, INPUT);
  pinMode(soilApin, INPUT);

  
  Serial.begin(9600); // send and receive at 9600 baud
}

void loop() {
  
  lightValue = analogRead(photoPin);
  lightPercent = (lightValue / 1023) * 100;
  
  tempValue = analogRead(tempPin);

  soilAnalog = analogRead(soilApin);

   //Voltage at pin in milliVolts = (reading from ADC) * (5000/1024)
  float tempVoltage = tempValue * 0.004882814;
  //Centigrade temperature = [(analog voltage in mV) - 500] / 10
  temperature = (tempVoltage - 0.5) * 100.0;

  Serial.println((String)lightPercent+';'+(String)temperature
            +';'+(String)soilAnalog);

  Serial.flush();

  delay(500);
}
