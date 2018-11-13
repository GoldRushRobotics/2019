/*
An Arduino code example for interfacing with the 
HDJD-S822-QR999 Color Sensor.  Put an object in front of the
sensor and look at the serial monitor to see the values the sensor
is reading.  Scaling factors and gains may have to be adjusted
for your application.

by: Jordan McConnell
 SparkFun Electronics
 created on: 1/24/12
 license: OSHW 1.0, http://freedomdefined.org/OSHW
 
Connect the gain pins of the sensor to digital pins 7 - 12 (or ground).
Connect the led pin to digital 13.
Connect Vr to analog 0, Vg to analog 1, and Vb to analog 2.
*/

// Define pins
const int ledpin = 13;
/*const int GSR1 = 12;
const int GSR0 = 11;
const int GSG1 = 10;
const int GSG0 = 9;
const int GSB1 = 8;
const int GSB0 = 7;*/

const int AVERAGE_AMOUNT=20;
const int BASE_COLOR=500;

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

void setup() 
{
  Serial.begin(9600);

  pinMode(ledpin, OUTPUT);
  //GSR1, GSR0, and GSB0 should be non-ground!!! XXGGGX
  
  /*pinMode(GSR1, OUTPUT);
  pinMode(GSR0, OUTPUT);
  pinMode(GSG1, OUTPUT);
  pinMode(GSG0, OUTPUT);
  pinMode(GSB1, OUTPUT);
  pinMode(GSB0, OUTPUT);*/

  // Turn on the LED
  digitalWrite(ledpin, HIGH);
  
  // Set the gain of each sensor
  /*digitalWrite(GSR1, LOW);
  digitalWrite(GSR0, LOW);
  digitalWrite(GSG1, LOW);
  digitalWrite(GSG0, LOW);
  digitalWrite(GSB1, LOW);
  digitalWrite(GSB0, LOW);*/
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
  vGreen = analogRead(greenpin) * 14;
  vBlue = analogRead(bluepin) * 17;
  redValue=((vRed*100)/16);
  greenValue=((vGreen*130)/22);
  blueValue=((vBlue*200)/25); 

  // Print values to the serial monitor
  
  //Serial.print("Red: ");
  //Serial.print(redValue, DEC);
  //Serial.print("\t\tGreen: ");
  //Serial.print(greenValue, DEC);
  //Serial.print("\tBlue: ");
  //Serial.println(blueValue, DEC);
  if(Raverage < 0) Raverage *= -1;
  if(Gaverage < 0) Gaverage *= -1;
  if(Baverage < 0) Baverage *= -1;
  
  Raverage += redValue;
  Gaverage += greenValue;
  Baverage += blueValue;
  
  delay(1);
  }
  
  Raverage /= AVERAGE_AMOUNT;
  Gaverage /= AVERAGE_AMOUNT;
  Baverage /= AVERAGE_AMOUNT;

  if(Raverage > BASE_COLOR || Gaverage > BASE_COLOR || Baverage > BASE_COLOR) {
    if(Raverage > Gaverage && Raverage > Baverage) {
      if(Gaverage > Baverage) Serial.println("YELLOW");
      else Serial.println("RED");
    }
    else if(Gaverage > Raverage && Gaverage > Baverage) Serial.println("GREEN");
    else Serial.println("BLUE");
  }
  else Serial.println("WHAT???");
  }
