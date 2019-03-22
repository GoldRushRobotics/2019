/*
First code by: Jordan McConnell
 SparkFun Electronics
 created on: 1/24/12
 license: OSHW 1.0, http://freedomdefined.org/OSHW
 
Heavily modified by William Daniels
To Do: fix the threshold value and add communication
*/

#include <Servo.h>
#include <math.h>

Servo left,right;
//Note that the servo motor must be externally powered, having the Arduino power the servo causes errors in the analog color sensor

const int AVERAGE_AMOUNT=50; //number of times to average color
const int BASE_COLOR=13;
//add ball base color

enum Color { RED, BLUE, GREEN, YELLOW, NONE };
Color reading = NONE;

int long Raverage;
int long Gaverage;
int long Baverage;

int long redpin = A2;
int long greenpin = A1;
int long bluepin = A0;

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

  left.attach(5);
  right.attach(6);
  left.write(0);
  right.write(0);

  pinMode(REDLED,OUTPUT);
  pinMode(BLUELED,OUTPUT);
  pinMode(GREENLED,OUTPUT);
  pinMode(13,OUTPUT);
  digitalWrite(13,HIGH);
 
}

void loop() 
{
  Raverage = 0;
  Gaverage = 0;
  Baverage = 0;
 //blue has become red and red has become blue?
  Baverage=analogRead(bluepin); //*1.1+2 //this is acting like red
  Raverage=analogRead(redpin); //this is acting like blue
  Gaverage=analogRead(greenpin); //-5
  
  Baverage=Baverage*2;
  Raverage=Raverage*1.5;
  Gaverage=Gaverage*1.3; 
  
  Serial.print(Baverage); //Raverage
  Serial.print(","); 
  Serial.print(Raverage); //Baverage
  Serial.print(",");
  Serial.println(Gaverage); //Gaverage
  
  if(Raverage > BASE_COLOR || Gaverage > BASE_COLOR || Baverage > BASE_COLOR) {
    if(Raverage > Gaverage && Raverage > Baverage) {
      //if(abs(Baverage - Gaverage) <= 5) {
         if(reading != RED) 
        {
          left.write(30);
          right.write(30);
          reading=RED;
          digitalWrite(REDLED,LOW);
          digitalWrite(BLUELED,HIGH);
          digitalWrite(GREENLED,HIGH);
        }
        //Serial.println(" RED");
        //}

    }
    else if(Gaverage > Raverage && Gaverage > Baverage) {
     if(Baverage > Raverage){
      if(reading != GREEN) 
        {
          left.write(40);
          right.write(40);
          reading=GREEN;
          digitalWrite(REDLED,HIGH);
          digitalWrite(BLUELED,HIGH);
          digitalWrite(GREENLED,LOW);
      }
      //Serial.println(" GREEN");
     }
      else {
        if(reading != YELLOW)  //120
        {
          left.write(60);
          right.write(60);
          reading=YELLOW;
          digitalWrite(REDLED,LOW);
          digitalWrite(BLUELED,HIGH);
          digitalWrite(GREENLED,LOW);
        }
        //Serial.println(" YELLOW"); 
      }
      
    }
    else /*if(Baverage > Raverage && Baverage > Gaverage)*/{
      //Serial.println("BLUE");
      if(reading != BLUE) 
      {
        left.write(90);
        right.write(90);
        reading=BLUE;
        digitalWrite(REDLED,HIGH);
        digitalWrite(BLUELED,LOW);
        digitalWrite(GREENLED,HIGH);
      }
      //Serial.println(" BLUE");
      }
    /*else {
          if(reading != YELLOW)  //120
        {
          left.write(-180);
          right.write(-180);
          reading=YELLOW;
          digitalWrite(REDLED,LOW);
          digitalWrite(BLUELED,HIGH);
          digitalWrite(GREENLED,LOW);
        }
        //Serial.println(" YELLOW");    
      }*/
  }  
      else {
        //Serial.println("WHAT???");
        if(reading != NONE) 
        {
        left.write(0);
        right.write(0);        
        reading=NONE;
        digitalWrite(REDLED,HIGH);
        digitalWrite(BLUELED,HIGH);
        digitalWrite(GREENLED,HIGH);
        //Serial.println(" NONE");   
      }
      } 
}
