#include <Servo.h>
#include <math.h>

Servo left,right;
//Note that the servo motor must be externally powered, having the Arduino power the servo causes errors in the analog color sensor

//const int AVERAGE_AMOUNT=50; //number of times to average color
const int BASE_COLOR=11;
//add ball base color

enum Color { RED, BLUE, GREEN, YELLOW, NONE };
Color reading = NONE;

int Raverage;
int Gaverage;
int Baverage;

const int redpin = A2;
const int greenpin = A1;
const int bluepin = A0;

const int ledPin = 13;

const int commPinLeft = 8;
const int commPinRight = 9;

const int RIGHT = 170;
const int LEFT = 30;

//GSX0 ground: Large drop
//GSX1 ground: Small drop
//GSX0 and GSX 1 ground: large gain
//Nothing needs to be tied to ground for our robot, though

const int REDLED=2;
const int BLUELED=3;
const int GREENLED=4;

int value = 0;
bool isRG = false;
bool isBY = false; //this isn't used in the conditional motor code but it does get used for input checking
//If we are red and blue, we will want to sort green and yellow into the dumping bins

void setup() 
{
  Serial.begin(9600);

  left.attach(5);
  right.attach(6);
  left.write(90);
  right.write(90);

  //initialize sensor pins
  pinMode(REDLED,OUTPUT);
  pinMode(BLUELED,OUTPUT);
  pinMode(GREENLED,OUTPUT);

  //turn on sensor LED
  pinMode(ledPin,OUTPUT);
  

  pinMode(commPinLeft,INPUT);
  pinMode(commPinRight,INPUT);

  while(!(isRG || isBY)) { //wait until we get an affirming signal
    isRG=digitalRead(commPinRight);
    isBY=digitalRead(commPinLeft);
    delay(100);
  }
  Serial.print("Panda communication says that isRG is ");
  value = isRG ? 1 : 0;
  Serial.println(value);
  digitalWrite(ledPin,HIGH);
}

void loop() 
{
  delay(100);
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
    if(Raverage > Gaverage && Raverage > Baverage) reading=RED;
    else if(Gaverage > Raverage && Gaverage > Baverage) {
      if(Baverage > Raverage) reading=GREEN;
      else {if(reading != YELLOW) reading=YELLOW;}    
    }
    else reading=BLUE;
    }  
    else reading=NONE;  

  switch(reading) {
    case RED:
        //max 175, 170 advised
        //min value 25, 30 advised
        if(isRG) {
          left.write(RIGHT); 
          right.write(RIGHT);           
        }
        else {
          left.write(LEFT); 
          right.write(LEFT);           
        }
        
        
        digitalWrite(REDLED,LOW);
        digitalWrite(BLUELED,HIGH);
        digitalWrite(GREENLED,HIGH);
        //Serial.println("RED");    
        break;

    case GREEN:
        if(isRG) {
          left.write(RIGHT); 
          right.write(RIGHT);           
        }
        else {
          left.write(LEFT); 
          right.write(LEFT);           
        }
        
        digitalWrite(REDLED,HIGH);
        digitalWrite(BLUELED,HIGH);
        digitalWrite(GREENLED,LOW);
        //Serial.println("GREEN");
        break;
    case YELLOW:
        if(isRG) {
          left.write(LEFT); 
          right.write(LEFT);           
        }
        else {
          left.write(RIGHT); 
          right.write(RIGHT);           
        }
        
        digitalWrite(REDLED,LOW);
        digitalWrite(BLUELED,HIGH);
        digitalWrite(GREENLED,LOW);
        //Serial.println("YELLOW");
        break; 

    case BLUE:
        if(isRG) {
          left.write(LEFT); 
          right.write(LEFT);           
        }
        else {
          left.write(RIGHT); 
          right.write(RIGHT);           
        }
        
        digitalWrite(REDLED,HIGH);
        digitalWrite(BLUELED,LOW);
        digitalWrite(GREENLED,HIGH);
        //Serial.println("BLUE");
        break;
        
    default:
    case NONE:
        left.write(90); 
        right.write(90);        
        digitalWrite(REDLED,HIGH);
        digitalWrite(BLUELED,HIGH);
        digitalWrite(GREENLED,HIGH);
        //Serial.println("NONE");
        break;   
  }
}
