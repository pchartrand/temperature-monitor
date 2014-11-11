const int referenceVolts = 5;
const int delayTime = 1000;
/* 
Assuming a third degree polynomial relationship between voltage
and temperature with a voltage divider made of an ntc 
thermistor (pullup) and a 5k6 resistor (to ground).
Voltage measured across the 5k6 resistor.

*/

const float a3 = 3.296;
const float b2 = -22.378;
const float c1 =  70.951;
const float d = -49.382;

void setup(){
  Serial.begin(9600);
}

void loop(){
  for(int in=0; in<2; in++){
    int val = analogRead(in);
    float volts = (val / 1023.0) * referenceVolts;
    float temp = a3*volts*volts*volts + b2*volts*volts + c1*volts + d;
    delay(delayTime);
    Serial.print(in);
    Serial.print(":");
    Serial.println(temp);
  }
}
