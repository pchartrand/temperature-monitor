#include <LiquidCrystal.h>

LiquidCrystal lcd(8, 13, 9, 4, 5, 6, 7);
const int referenceVolts = 5;
const int delayTime = 1000;
const int number_of_sensors = 5;

float temps[number_of_sensors];

          
/* 
Assuming a third degree polynomial relationship between voltage
and temperature with a voltage divider made of an ntc 
thermistor (pullup) and a 5k6 resistor (to ground).
Voltage measured across the 5k6 resistor.

*/

const float a3 = 1.669;
const float b2 = -10.809;
const float c1 =  41.851;
const float d = -25.581;
const int first_input = 1;

void setup(){
  Serial.begin(9600);
  lcd.begin(16, 2);
}

float getTemp(int in){
  int val = analogRead(in);
  float volts = (val / 1023.0) * referenceVolts;
  return a3*volts*volts*volts + b2*volts*volts + c1*volts + d;   
}

void reportTemp(int in, float temp){
  Serial.print(in - 1);
  Serial.print(":");
  Serial.println(temp);
  
}

void displayTemps(){
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(temps[0], 1);
  lcd.setCursor(6, 0);
  lcd.print(temps[1], 1);
  lcd.setCursor(12, 0);
  lcd.print(temps[2], 1);
  lcd.setCursor(0, 1);
  lcd.print(temps[3], 1);
  lcd.setCursor(6, 1);
  lcd.print(temps[4], 1);
}

void loop(){
  float temp;
  for(int i=0; i < number_of_sensors; i++){
    int input = i + first_input;
    temp = getTemp(input);
    temps[i] = temp;
    delay(delayTime);
    reportTemp(input, temp);
  }
  displayTemps();
}
