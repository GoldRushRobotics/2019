/*
First code by: Jordan McConnell
 SparkFun Electronics
 created on: 1/24/12
 license: OSHW 1.0, http://freedomdefined.org/OSHW
 
Heavily modified by William Daniels

To Dew:
Fix shiny ball reading
Get LEDS for ball reading
*/

#include <Servo.h>

Servo myservo;

const int AVERAGE_AMOUNT=20; //number of times to average color
const int BASE_COLOR=100;
//add ball base color

enum Color { RED, BLUE, GREEN, YELLOW, NONE };
Color reading = NONE;

int Raverage;
int Gaverage;
int Baverage;

int redpin = A0;
int greenpin = A1;
int bluepin = A2;

// Sensor read values
int vRed = 0;
int vGreen = 0;
int vBlue = 0;
int redValue, greenValue, blueValue = 0;

  //GSX0 ground: Large drop
  //GSX1 ground: Small drop
  //GSX0 and GSX 1 ground: large gain
  //Nothing needs to be tied to ground, though
void setup() 
{
  Serial.begin(9600);

  myservo.attach(9);
  myservo.write(0);
}

void loop() 
{
  Raverage = 0;
  Gaverage = 0;
  Baverage = 0;
  
  for(int i=0;i<AVERAGE_AMOUNT;i++) {
  // Read sensors
  // On page 7 of the datasheet, there is a graph of the 
  // spectral responsivity of the chip.  Scaling factors were
  // selected based on this graph so that the gain of each 
  // color is closer to being equal
  vRed = analogRead(redpin) * 10;
  vGreen = analogRead(greenpin) * 10; //14
  vBlue = analogRead(bluepin) * 10;//17

  if(vRed < 0) vRed *= -1;
  if(vGreen < 0) vGreen *= -1;
  if(vBlue < 0) vBlue *= -1;

  redValue=vRed;
  greenValue=vGreen/2;
  blueValue=vBlue;
  
  
  //old scale values
  //redValue=((vRed*100)/2);
  //greenValue=((vGreen*130)/4);
  //blueValue=((vBlue*200)/8); 
  
  Raverage += redValue;
  Gaverage += greenValue;
  Baverage += blueValue;
  
  delay(1);
  }
  
  Raverage /= AVERAGE_AMOUNT;
  Gaverage /= AVERAGE_AMOUNT;
  Baverage /= AVERAGE_AMOUNT;
  /*Serial.print(Baverage);
  Serial.print(",");
  Serial.print(Raverage);
  Serial.print(",");
  Serial.println(Gaverage);*/

  if(Raverage > BASE_COLOR || Gaverage > BASE_COLOR || Baverage > BASE_COLOR) {
    if(Raverage > Gaverage && Raverage > Baverage) {
      if(abs(Baverage - Gaverage) >= 30) {
        Serial.println("YELLOW");
        if(reading != YELLOW) myservo.write(120);
        reading=YELLOW;
        }
      else {
        Serial.println("RED");
        if(reading != RED) myservo.write(90);
        reading=RED;
        }
    }
    else if(Gaverage > Raverage && Gaverage > Baverage) {
      Serial.println("GREEN");
      if(reading != GREEN) myservo.write(90);
      reading=GREEN;
      }
    else {
      Serial.println("BLUE");
      if(reading != BLUE) myservo.write(60);
      reading=BLUE;
      }
  }  
      else {
        Serial.println("WHAT???");
        if(reading != NONE) myservo.write(90);
        reading=NONE;
        }
  }
