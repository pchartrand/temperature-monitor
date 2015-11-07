const int referenceVolts = 5;
const int delayTime = 1000;
const int number_of_sensors = 5;
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


void setup(){
  Serial.begin(9600);
}

float getTemp(int in){
  int val = analogRead(in);
  float volts = (val / 1023.0) * referenceVolts;
  return a3*volts*volts*volts + b2*volts*volts + c1*volts + d;   
}

void reportTemp(int in, float temp){
  Serial.print(in);
  Serial.print(":");
  Serial.println(temp);
}

void loop(){
  float temp;
  for(int in=0; in<number_of_sensors; in++){
    temp = getTemp(in);
    delay(delayTime);
    reportTemp(in, temp);
  }
}
