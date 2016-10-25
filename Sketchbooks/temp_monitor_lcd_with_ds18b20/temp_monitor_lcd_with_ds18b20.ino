#include <LiquidCrystal.h>
#include <LCDKeypad.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#define ONE_WIRE_BUS 2
#define LCD_BACKLIGHT_PIN         10
#define LCD_BACKLIGHT_OFF()     digitalWrite( LCD_BACKLIGHT_PIN, LOW )
#define LCD_BACKLIGHT_ON()      digitalWrite( LCD_BACKLIGHT_PIN, HIGH )

LiquidCrystal lcd(8, 13, 9, 4, 5, 6, 7);
const int referenceVolts = 5;
const int delayTime = 950;
const int debounceTime = 50;
const int number_of_sensors = 5;
float temps[number_of_sensors+1];
float volts[number_of_sensors];
int values[number_of_sensors];
float oldTemp = 0.0;

const int NUM_KEYS = 5;
int adc_key_val[5] ={50, 200, 400, 600, 800 };
int key=-1;
int oldkey=-1;
char msgs[5][17] = {"   Numerique    ",
                    "     Celsius    ",               
                    "    Farenheit   ",
                    "      Volts     ",
                    "     Celsius    " };
                    
const int LCD_ENABLE = 9;
int display_on_time = 0;

          
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

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void(* resetFunc) (void) = 0;

void setup(){
  Serial.begin(9600);
  lcd.begin(16, 2);
  digitalWrite( LCD_BACKLIGHT_PIN, HIGH );
  pinMode( LCD_BACKLIGHT_PIN, OUTPUT ); 
  sensors.begin();
  int nbSensors;
  nbSensors = sensors.getDeviceCount();
  //Serial.print("Number of sensors found: ");
  //Serial.println(nbSensors);
}


float getVolt(int val){
  return (val / 1023.0) * referenceVolts;
}

float getTemp(float volts){
  return a3*volts*volts*volts + b2*volts*volts + c1*volts + d;   
}

void reportTemp(int in, float temp){
  Serial.print(in - 1);
  Serial.print(":");
  Serial.println(temp);
  
}

void displayValues(){
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(values[0]);
  lcd.setCursor(6, 0);
  lcd.print(values[1]);
  lcd.setCursor(12, 0);
  lcd.print(values[2]);
  lcd.setCursor(0, 1);
  lcd.print(values[3]);
  lcd.setCursor(6, 1);
  lcd.print(values[4]);
  lcd.setCursor(12, 1);
  lcd.print("1024");
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
  lcd.setCursor(12, 1);
  lcd.print(temps[5],1);
}

float cToF(float c){
  return (c * 9 / 5) + 32;
}
  
void displayFarenheits(){
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(cToF(temps[0]), 1);
  lcd.setCursor(6, 0);
  lcd.print(cToF(temps[1]), 1);
  lcd.setCursor(12, 0);
  lcd.print(cToF(temps[2]), 1);
  lcd.setCursor(0, 1);
  lcd.print(cToF(temps[3]), 1);
  lcd.setCursor(6, 1);
  lcd.print(cToF(temps[4]), 1);
  lcd.setCursor(12, 1);
  lcd.print(cToF(temps[5]), 1);
}
void displayVolts(){
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(volts[0], 2);
  lcd.setCursor(6, 0);
  lcd.print(volts[1], 2);
  lcd.setCursor(12, 0);
  lcd.print(volts[2], 2);
  lcd.setCursor(0, 1);
  lcd.print(volts[3], 2);
  lcd.setCursor(6, 1);
  lcd.print(volts[4], 2);
  lcd.setCursor(12, 1);
  lcd.print("   V");
}

int get_key(unsigned int input)
{
    int k;
    for (k = 0; k < NUM_KEYS; k++){
      if (input < adc_key_val[k]){
        return k;
      }
    }   
    if (k >= NUM_KEYS)k = -1;  // No valid key pressed
    return k;
}

int getKeypress(){
  int adc_key_in = analogRead(0);    // read the value from the sensor 
   key = get_key(adc_key_in);  // convert into key press
   if (key != oldkey)   // if keypress is detected
   {
     delay(debounceTime);
     adc_key_in = analogRead(0);    // read the value from the sensor 
     key = get_key(adc_key_in);    // convert into key press
     if (key != oldkey)    
     {   
       lcd.clear();
       lcd.setCursor(0, 1);
       oldkey = key;
       if (key >=0)
       {
           lcd.print(msgs[key]);            
       }
     }
   }
   return key;
}

void loop(){
  float temp;
  float volt;
  if (display_on_time > 15){
      lcd.noDisplay();
  }
  if (display_on_time > 20){
      LCD_BACKLIGHT_OFF();
  }
  for(int i=0; i < number_of_sensors; i++){
    key = getKeypress();
    if (key > 0){
      display_on_time = 0;
      LCD_BACKLIGHT_ON();
      lcd.display();
    }
    int input = i + first_input;
    int value = analogRead(input);
    volt = getVolt(value);
    temp = getTemp(volt);
    values[i] = value;
    temps[i] = temp;
    volts[i] = volt;
    delay(delayTime);
    reportTemp(input, temp);
    display_on_time += 1;
  }
  sensors.requestTemperatures();
  float newTemp = sensors.getTempCByIndex(0);
  delay(250);
  if (newTemp < 55.0){
    temp = newTemp;
    oldTemp = temp;
  }else{
    temp = oldTemp;
  }
  temps[number_of_sensors] = temp;  
  reportTemp(number_of_sensors+1, temp);
  
  if(key == 0){
   displayValues();
  }else if(key == 2){
    displayFarenheits();
  }else if(key == 3){
    displayVolts();
  }else{
    displayTemps();
  }
}
