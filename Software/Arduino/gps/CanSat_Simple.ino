#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP085_U.h>
#include <Adafruit_ADXL345_U.h>
#include <Adafruit_HMC5883_U.h>
/*---------------------------------------------------------------*/
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(1234);
Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345);
Adafruit_BMP085_Unified bmp = Adafruit_BMP085_Unified(10085);
long s, r;
float altMax = 0;
/*--------------------------------------------------------------*/

void setup(void){
  Serial.begin(115200);
  accel.setRange(ADXL345_RANGE_16_G);
}

void loop(void){
  sensors_event_t event;
  sensors_event_t event1; 
  sensors_event_t event2;
    
    s = millis();
    while(1){
      if(!bmp.begin() or !accel.begin() or !mag.begin()){
        break;
        }
        bmp.getEvent(&event);
        mag.getEvent(&event1);
        accel.getEvent(&event2);
        
        float temperature;
        bmp.getTemperature(&temperature);
        float seaLevelPressure = SENSORS_PRESSURE_SEALEVELHPA;
    
        float heading = atan2(event1.magnetic.y, event1.magnetic.x);
        float declinationAngle = 0.22;
        heading += declinationAngle;
        if(heading < 0)
          heading += 2*PI;
        if(heading > 2*PI)
          heading -= 2*PI;

        float Z = event2.acceleration.z;

        float altitud = bmp.pressureToAltitude(seaLevelPressure, event.pressure);
        
        Serial.print(temperature); Serial.print(","); //ºC
        Serial.print(event.pressure); Serial.print(",");//hPa
        Serial.print(altitud); Serial.print(",");//msnm
        Serial.print(heading); Serial.print(",");//Radianes
        Serial.print(Z); Serial.print(","); // m/s^2
        r = (millis())-s;
        Serial.println(r);
        
        if(altMax < altitud){
          altMax = altitud;
          }
        delay(50);
     }
 }
