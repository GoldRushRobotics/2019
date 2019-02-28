/*
First code by: Jordan McConnell
 SparkFun Electronics
 created on: 1/24/12
 license: OSHW 1.0, http://freedomdefined.org/OSHW
 
Heavily modified by William Daniels

To Dew: Fix yellow
*/

#include <Servo.h>
#include <math.h>

Servo myservo;
//Note that the servo motor must be externally powered, having the Arduino power the servo causes errors in the analog color sensor

const int AVERAGE_AMOUNT=50; //number of times to average color
const int BASE_COLOR=13;
//add ball base color

enum Color { RED, BLUE, GREEN, YELLOW, NONE };
Color reading = NONE;

int long Raverage;
int long Gaverage;
int long Baverage;

int long redpin = A0;
int long greenpin = A1;
int long bluepin = A2;

// Sensor read values
int vRed = 0;
int vGreen = 0;
int vBlue = 0;
int redValue, greenValue, blueValue = 0;

  //GSX0 ground: Large drop
  //GSX1 ground: Small drop
  //GSX0 and GSX 1 ground: large gain
  //Nothing needs to be tied to ground, though

  const int REDLED=2;
  const int BLUELED=3;
  const int GREENLED=4;

  int value = 0;
  bool isRB = false;
  //If we are red and blue, we will want to sort green and yellow into the dumping bins
  
void setup() 
{
  Serial.begin(9600);

  myservo.attach(9);
  myservo.write(0);

  pinMode(REDLED,OUTPUT);
  pinMode(BLUELED,OUTPUT);
  pinMode(GREENLED,OUTPUT);
 
}

void loop() 
{
  Raverage = 0;
  Gaverage = 0;
  Baverage = 0;

  Baverage=analogRead(bluepin)*1.1+2;
  Raverage=analogRead(redpin);
  Gaverage=analogRead(greenpin)-5;
  
  Serial.print(analogRead(bluepin)*1.1+2); //Baverage
  Serial.print(",");
  Serial.print(analogRead(redpin)); //Raverage
  Serial.print(",");
  Serial.println(analogRead(greenpin)-5); //Gaverage

  if(Raverage > BASE_COLOR || Gaverage > BASE_COLOR || Baverage > BASE_COLOR) {
    if(Raverage > Gaverage && Raverage > Baverage) {
      if(abs(Baverage - Gaverage) <= 5) {
         if(reading != RED) 
        {
          myservo.write(90);
          reading=RED;
          digitalWrite(REDLED,LOW);
          digitalWrite(BLUELED,HIGH);
          digitalWrite(GREENLED,HIGH);
        }
        }

    }
    else if(Gaverage > Raverage && Gaverage > Baverage) {
      if(reading != GREEN) 
      {
        myservo.write(180);
        reading=GREEN;
        digitalWrite(REDLED,HIGH);
        digitalWrite(BLUELED,HIGH);
        digitalWrite(GREENLED,LOW);
      }
      }
    else if(Baverage > Raverage && Baverage > Gaverage){
      //Serial.println("BLUE");
      if(reading != BLUE) 
      {
        myservo.write(90);
        reading=BLUE;
        digitalWrite(REDLED,HIGH);
        digitalWrite(BLUELED,LOW);
        digitalWrite(GREENLED,HIGH);
      }
      }
    else {
          if(reading != YELLOW)  //120
        {
          myservo.write(0);
          reading=YELLOW;
          digitalWrite(REDLED,LOW);
          digitalWrite(BLUELED,HIGH);
          digitalWrite(GREENLED,LOW);
        }    
      }
  }  
      else {
        //Serial.println("WHAT???");
        if(reading != NONE) 
        {
        myservo.write(90);        
        reading=NONE;
        digitalWrite(REDLED,HIGH);
        digitalWrite(BLUELED,HIGH);
        digitalWrite(GREENLED,HIGH);
      }
      } 
}
