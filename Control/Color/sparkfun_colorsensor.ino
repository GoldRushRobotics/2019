//Servo motors:
#include <Servo.h> //We need the servo library for the sorting arms
Servo left,right; //Even though the servos will both go in the same direction, I have defined both of them here just in case

//Color enumeration
enum Color { RED, BLUE, GREEN, YELLOW, NONE }; //Enumerations are cool
Color reading = NONE; //This enumeration is used to store which color we see

//Defining constants
const int MINIMUM_VALUE=11; //A color must be detected over this analog value for an object to be counted

const int RED_PIN = A2; //These are where the color sensor's 3 output pins for color values should go
const int GREEN_PIN = A1;
const int BLUE_PIN = A0;

const int LED_PIN = 13; //Pin 13 goes to the sensor's LED

const int COMMUNICATION_LEFT = 8; //These two pins are used for "talking" with the Late Panda
const int COMMUNICATION_RIGHT = 9; //They are not serial, they simply receive digital values

const int CENTER = 90; //These constants are for positioning the motors
const int RIGHT = 170; //max 175, 170 advised
const int LEFT = 30; //min value 25, 30 advised

const int REDLED = 12; //These are for controling the RGB LED
const int GREENLED = 11; //The digitalWrite() values associated with these pins are active low
const int BLUELED = 10; //since we had common annode LEDs

const int MOTOR_DELAY = 500; //This determines how long the motor stays on a certain color, and is also used to determine the length of the DELAY case
const int NONE_DELAY = 500; //This determines how long a NONE case lasts

//GSX0 ground: Large drop
//GSX1 ground: Small drop
//GSX0 and GSX 1 ground: large gain
//Nothing needs to be tied to ground for our robot, though

Color nextColor = NONE; //these are used to pad out the input, add more of these variables to pad out how long the delay is
//Color nextColor1 = NONE; //I didn't want to fiddle around with arrays, so just keep adding nextColor#'s if somehow this delay isn't long enough (tested with NONE_DELAY = 500 and it worked pretty well pre-mount

int redValue; //These are the values that will store the color values read from the sensor
int greenValue; //They will also store the scaled values, which will be compared against each other to decide color
int blueValue;

bool isRB = false; //This is for storing which team we are on, in the conditional motor code
bool isGY = false; //This variable isn't used in the conditional motor code but it does get used for input checking
//If we are red and blue, we will want to sort green and yellow into the dumping bins

void setup() 
{
  //Initialize the inputBuffer array
  //for(int i=0;i<=(BUFFER_LENGTH-1);i++) inputBuffer[i] = NONE;
  
  Serial.begin(9600);

  //Set up motors
  left.attach(5);
  right.attach(6);
  left.write(90);
  right.write(90);

  //initialize sensor pins
  pinMode(REDLED,OUTPUT);
  pinMode(BLUELED,OUTPUT);
  pinMode(GREENLED,OUTPUT);

  //Configure the sensor's LED but don't turn it on yet
  pinMode(LED_PIN,OUTPUT);

  //Set up the communication pins
  pinMode(COMMUNICATION_LEFT,INPUT);
  pinMode(COMMUNICATION_RIGHT,INPUT);

  //Receive team state based on communication pins
  while(!(isRB || isGY)) { //wait until we get an affirming signal
    isRB = digitalRead(COMMUNICATION_RIGHT);
    isGY = digitalRead(COMMUNICATION_LEFT);
    delay(100);
  }
  
  //DEBUG: used for checking communication
  /*
  Serial.print("Panda communication says that isRB is ");
  if(isRB) Serial.println("1");
  else Serial.println("0");
  */
  
  //Turn on sensor's LED to signify that we're ready to sort
  digitalWrite(LED_PIN,HIGH); 
  
}

void loop() 
{
  //Read in colors
  blueValue = analogRead(BLUE_PIN);
  redValue = analogRead(RED_PIN);
  greenValue = analogRead(GREEN_PIN);

  //Scale values
  blueValue *= 2;
  redValue *= 1.5;
  greenValue *= 1.3; 

  //DEBUG: Serial plotter code
  //The order is blue, red, green because of the serial plotter's weirdness
  /*
  Serial.print(blueValue);
  Serial.print(","); 
  Serial.print(redValue);
  Serial.print(",");
  Serial.println(greenValue);
  */
  
  //inputBuffer[arrayIndexCount] = determineColor;
  sortColor(nextColor);
  //nextColor = nextColor1;
  nextColor = determineColor(redValue,greenValue,blueValue) ;  
}


Color determineColor(int red, int green, int blue) { //rgb
  if(redValue > MINIMUM_VALUE || greenValue > MINIMUM_VALUE || blueValue > MINIMUM_VALUE) {
  //If any of the readings are above the minimum detection threshold (MINIMUM_VALUE)...
    if(redValue > greenValue && redValue > blueValue) return RED;
    //...then see if red is the most reflected color, and if not...
    else if(greenValue > redValue && greenValue > blueValue) {
    //...then see if green is the most reflected color.  
      if(blueValue > redValue) return GREEN;
      //If there is more blue reflected than red (green > blue > red) then the object is green.
      else return YELLOW; //{if(reading != YELLOW)   }
      //Otherwise, the object is a mix of green and red and thus is yellow.
    }
    else return BLUE;
    //If the object isn't reflecting mostly red or mostly green, then it must be blue.
    }  
  else return NONE;  
  //Otherwise, there must not be any object in front of the sensor because there isn't enough color being reflected.
}


//Motor and LED control switch statement method
void sortColor(Color food) { //Takes in the enumeration type Color
    switch(food) {
    case RED:
        if(isRB) {
          left.write(CENTER); 
          right.write(CENTER);           
        }
        else {
          left.write(LEFT); 
          right.write(LEFT);           
        }       
        
        digitalWrite(REDLED,LOW); //Remember: active low for common annode LEDs
        digitalWrite(BLUELED,HIGH);
        digitalWrite(GREENLED,HIGH);
        delay(MOTOR_DELAY); //hang out on this motor setting for a while so that the motor's don't freak out
        Serial.println("RED");    
        break;

    case GREEN:
        if(isRB) {
          left.write(RIGHT); 
          right.write(RIGHT);           
        }
        else {
          left.write(CENTER); 
          right.write(CENTER);           
        }
        
        digitalWrite(REDLED,HIGH);
        digitalWrite(BLUELED,HIGH);
        digitalWrite(GREENLED,LOW);
        delay(MOTOR_DELAY);
        Serial.println("GREEN");
        break;
        
    case YELLOW:
        if(isRB) {
          left.write(LEFT); 
          right.write(LEFT);           
        }
        else {
          left.write(CENTER); 
          right.write(CENTER);           
        }
        
        digitalWrite(REDLED,LOW);
        digitalWrite(BLUELED,HIGH);
        digitalWrite(GREENLED,LOW);
        delay(MOTOR_DELAY);
        Serial.println("YELLOW");
        break; 

    case BLUE:
        if(isRB) {
          left.write(CENTER); 
          right.write(CENTER);           
        }
        else {
          left.write(RIGHT); 
          right.write(RIGHT);           
        }
        
        digitalWrite(REDLED,HIGH);
        digitalWrite(BLUELED,LOW);
        digitalWrite(GREENLED,HIGH);
        delay(MOTOR_DELAY);
        Serial.println("BLUE");
        break;

    default:        
    case NONE:
        left.write(CENTER); 
        right.write(CENTER);        
        digitalWrite(REDLED,HIGH);
        digitalWrite(BLUELED,HIGH);
        digitalWrite(GREENLED,HIGH);
        Serial.println("NONE");
        delay(NONE_DELAY); //Having a little delay increases accuracy for detecting yellow/green correctly, but this can be removed if need be
        break;   
  }
}



//Prototype code for queueing shapes

//int arrayIndexCount = 0; //This will repeatedly count from 0 to 9 and will point to where we should put the next color object. 

//Buffer space options (DELAY time amount is further down (DELAY_DELAY))
//Color inputBuffer[BUFFER_LENGTH];
//int const BUFFER_LENGTH = 5; //Total number of elements in the buffer array
//const int COLOR_SPACING = 1; //Experimental

/*case DELAY;
    
        //Delay and Default are the only cases which do not alter the motor's previous state
        digitalWrite(REDLED,LOW); //We also set the LED to white to indicate that we are waiting/are in big trouble (default case=bad)
        digitalWrite(BLUELED,LOW);
        digitalWrite(GREENLED,LOW);
        delay(MOTOR_DELAY);
    break;*/
