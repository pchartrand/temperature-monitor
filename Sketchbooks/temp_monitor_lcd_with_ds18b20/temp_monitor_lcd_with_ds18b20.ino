#include <LiquidCrystal.h>
#include <LCDKeypad.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define REFERENCE_VOLTS 5
#define NUMBER_OF_SENSORS 5
#define FIRST_NTC_INPUT 1
#define DELAY_TIME 950

#define LCD_ENABLE 9
#define LCD_BACKLIGHT_PIN         10
#define LCD_BACKLIGHT_OFF()     digitalWrite( LCD_BACKLIGHT_PIN, LOW )
#define LCD_BACKLIGHT_ON()      digitalWrite( LCD_BACKLIGHT_PIN, HIGH )

#define NUMBER_OF_KEYS 5
#define KEY_READ_INPUT 0
#define KEY_DEBOUNCE_TIME 50

#define ONE_WIRE_BUS 2
#define DS18B20_SLEEPTIME 248
#define DS18B20_ONEWIRE_INDEX 0

const float DS18B20_NOT_READY = 85.0;

char MEASUREMENT_UNITS[5][17] = {
    "   Numerique    ",
    "     Celsius    ",               
    "    Farenheit   ",
    "      Volts     ",
    "     Celsius    " 
};

int ADC_KEY_VALS[5] = { 50, 200, 400, 600, 800 };

int key=-1;
int oldkey=-1;

float volts[NUMBER_OF_SENSORS];
int values[NUMBER_OF_SENSORS];
float temps[NUMBER_OF_SENSORS + 1];

float lastTempReading = 0.0;                    
int displayOnTime = 0;

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

LiquidCrystal lcd(8, 13, 9, 4, 5, 6, 7);
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void(* resetFunc) (void) = 0;

float getVolt(int val){
  return (val / 1023.0) * REFERENCE_VOLTS;
}

float getTemp(float volts){
  return a3*pow(volts, 3) + b2*pow(volts, 2) + c1*volts + d;   
}

float cToF(float c){
  return (c * 9 / 5) + 32.0;
}

void reportTemp(int in, float temp){
  Serial.print(in - 1);
  Serial.print(":");
  Serial.println(temp);
}

void displayRawValues(){
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

void displayCelsiuses(){
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

int getKey(unsigned int input){
    int k;
    for (k = 0; k < NUMBER_OF_KEYS; k++){
      if (input < ADC_KEY_VALS[k]){
        return k;
      }
    }   
    if (k >= NUMBER_OF_KEYS)k = -1;  // No valid key pressed
    return k;
}

int getKeypress(){
  int adcKeyIn = analogRead(KEY_READ_INPUT);
   key = getKey(adcKeyIn);
   if (key != oldkey){
     delay(KEY_DEBOUNCE_TIME);
     adcKeyIn = analogRead(KEY_READ_INPUT); 
     key = getKey(adcKeyIn);
     if (key != oldkey){   
       lcd.clear();
       lcd.setCursor(0, 1);
       oldkey = key;
       if (key >= 0){
           lcd.print(MEASUREMENT_UNITS[key]);            
       }
     }
   }
   return key;
}

void setup(){
  Serial.begin(9600);
  lcd.begin(16, 2);
  digitalWrite( LCD_BACKLIGHT_PIN, HIGH );
  pinMode( LCD_BACKLIGHT_PIN, OUTPUT ); 
  sensors.begin();
  int nbSensors;
  nbSensors = sensors.getDeviceCount();
  lcd.print("Nb. of sensors");
  lcd.setCursor(7, 1);
  lcd.print(nbSensors);
}

void loop(){
  float temp;
  float volt;
  if (displayOnTime > 15){
      lcd.noDisplay();
  }
  if (displayOnTime > 20){
      LCD_BACKLIGHT_OFF();
  }
  for(int i = 0; i < NUMBER_OF_SENSORS; i++){
    key = getKeypress();
    if (key > 0){
      displayOnTime = 0;
      LCD_BACKLIGHT_ON();
      lcd.display();
    }
    int input = i + FIRST_NTC_INPUT;
    int value = analogRead(input);
    volt = getVolt(value);
    temp = getTemp(volt);
    values[i] = value;
    temps[i] = temp;
    volts[i] = volt;
    delay(DELAY_TIME);
    reportTemp(input, temp);
    displayOnTime += 1;
  }
  sensors.requestTemperatures();
  float newTemp = sensors.getTempCByIndex(DS18B20_ONEWIRE_INDEX);
  delay(DS18B20_SLEEPTIME);
  if (newTemp < DS18B20_NOT_READY){
    temp = newTemp;
    lastTempReading = temp;
  }else{
    temp = lastTempReading;
  }
  temps[NUMBER_OF_SENSORS] = temp;  
  reportTemp(NUMBER_OF_SENSORS+1, temp);
  
  if(key == 0){
   displayRawValues();
  }else if(key == 2){
    displayFarenheits();
  }else if(key == 3){
    displayVolts();
  }else{
    displayCelsiuses();
  }
}
