// R3: Jan 23, 2019: Basic functionality     -Greg Lewis
// R4: Jan 23, 2019: Smooth control          -Greg Lewis
// R5L Feb 2, 2019: WASD and Int implementation over serial   -Matt Wells
// R6: Feb 8, 2019: Many Major updates:      -Greg Lewis

                //   Restructure turning to enable the bot to turn in place
                //   Human readable turn commands added (f,b,l,r)
                //   Out of range detection. Motors don't rollover from of full on to off and vice versa
                //   Major restructuring of the move() function to be more efficient and more robust. Accounts for edge cases
                //   Comprehensive documentation of move()
// R9: Mar 25, 2019:  Kill switches introduced

#include <Servo.h>

//DRIVE MOTORS//
#define rightSpd 5  // PWM Magnitude
#define rightDir 4  // Digital direction
#define leftSpd 6
#define leftDir 7
//FEED MOTORS//
#define frontFeedSpd 9
#define frontFeedDir 12
#define rampFeedSpd 10
#define rampFeedDir 8
//COLORUINO COMM//
#define homeSendPin1 18
#define homeSendPin2 19
//KILL SWITCH//
#define killSwitchPin1 22
#define killSwitchPin2 23
//SERVOS//
#define LEFT_SERVO_PIN 13
#define RIGHT_SERVO_PIN 11

const int DUMP_VAL_LEFT = 10;
const int HOME_VAL_LEFT = 101;
const int DUMP_VAL_RIGHT = 140;
const int HOME_VAL_RIGHT = 53;

Servo left, right;
char mode, servoSide;

int speed = 0;     //0 = velocity, 1 = turn
int direction = 0;
int speedStep = 1;
int directionStep = 1;
int nullRange = 5;      // Lower threshold of when a wheel tries to turn
                        //This is a power saving feature

void move(int velocity, int turn);  //Declare the main movement funtion
void dump(char);
void setup(void)
{
  Serial.begin(115200);
  Serial.println("setup");
  pinMode(rightSpd, OUTPUT);
  pinMode(rightDir, OUTPUT);
  pinMode(leftSpd, OUTPUT);
  pinMode(leftDir, OUTPUT);
  pinMode(frontFeedSpd, OUTPUT);
  pinMode(frontFeedDir, OUTPUT);
  pinMode(homeSendPin1, OUTPUT);
  pinMode(homeSendPin2, OUTPUT);
  pinMode(killSwitchPin1, INPUT_PULLUP);
  pinMode(killSwitchPin2, INPUT_PULLUP);

  left.attach(LEFT_SERVO_PIN);
  left.write(HOME_VAL_LEFT);
  right.attach(RIGHT_SERVO_PIN);
  right.write(HOME_VAL_RIGHT);

  digitalWrite(frontFeedSpd, HIGH);
  digitalWrite(frontFeedDir, HIGH);
}

bool killSwitchPressed = false;

void loop(void){
  
  int val = 0;
  char mode = 0, base;
  
  while(Serial.available() <= 0);

  do {
    int killSwitchState = digitalRead(killSwitchPin1) && digitalRead(killSwitchPin2);
    if (killSwitchState == 0 && !killSwitchPressed){
      move(-50,0);
      delay(500);
      move(0,0);
      speed = 0; direction = 0;
      killSwitchPressed = true;
    } else {
      mode = Serial.read();
    }
    
  } while(mode != 'w' && mode != 'a' && mode != 's' && mode != 'd' && mode != 'z' && mode != 'h' && mode != 'p' && mode != 'f');

  while(Serial.available() <= 0);

  if (mode == 'p'){
    servoSide = Serial.read();
  } else if (mode == 'h'){
    base = Serial.read();
  } else {
    val = Serial.parseInt();
  }

   killSwitchPressed = false;

  //Serial.println(mode);
  //Serial.println(val);
  
  switch(mode){
    case 'w': speed = val; break; //straight
    case 'l':
    case 'a': direction = -val; break; //left
    case 'b':
    case 's': speed = -val; break; //backwards
    case 'r':
    case 'd': direction = val; break; //right
    case 'z': speed = 0; direction = 0; break; //stop
    case 'h':
      switch(base){
        case 'r': 
        case 'b':
                val = 1;
                break;
        case 'g':
        case 'y':
                val = 0;
                break;
      }
      digitalWrite(val, homeSendPin1);
      digitalWrite(!val, homeSendPin2); 
      break;
    case 'p': dump(servoSide); break;
    case 'f':
      if (val == 1 || val == 0){
        digitalWrite(frontFeedSpd, val);
        digitalWrite(frontFeedDir, HIGH);
      } else {
        digitalWrite(frontFeedSpd, HIGH);
        digitalWrite(frontFeedDir, LOW);
      }
      break;
  }
    
  move(speed, direction);
  
}

int sign(int val){
  if (val > 0) return 1;
  else if (val < 0) return 0;
  else return 0;
}

void move(int velocity, int turn){  
  // This function translates the desired speed and direction into wheel motion
  // It takes the desired direction and velocity and translates it for the motor driver hardware
  // Basic functionality:
  // Split the velocity to each wheel
  // Add or subtract from the foreward / backward wheel speed to turn
  // Filter the calculated values so that they are in the acceptable range
  // Filter the calculated values so that the motors don't try to turn when they can't move the motors
  // Output the final direction and speed information to the hardware

  int leftVelocity;                 // A wheel specific speed (rotation rate) to be adjusted independently of the other wheel
  int rightVelocity;                // Same on the other wheel
  int turnChange = turn * 0.5;      // Get the amount for each wheel to adjust l/r direction (two wheels * 0.5)
  
  leftVelocity = velocity;    // Initialize the speed before calculating turn
  rightVelocity = velocity;   // Same on the other wheel
  

// This section adjusts the individual wheel velocities to account for turning
  if(turn > 0){                   //If we are turning right
    leftVelocity += turnChange;   //Adjust speed of left wheel so it turns right
    rightVelocity -= turnChange; //Also adjust the speed of the right wheel as well for more precise turning
  }
  else if(turn < 0){              // Same on the other wheel
    
    leftVelocity += turnChange;
    rightVelocity -= turnChange;
  }


    // This section limits the wheel values to the desired range
    if((rightVelocity > 255) || (rightVelocity < -255)){
      rightVelocity = 255 * sign(rightVelocity);
    }
    if(leftVelocity > 255 || leftVelocity < -255){
        leftVelocity = 255 * sign(leftVelocity);
    }


    // Keep from trying to drive the motors at very low speeds to save power
    if(abs(rightVelocity) < nullRange){ // If the velocity to output is small enough (within the nullRange),
        rightVelocity = 0;              // Don't try to turn it.
    }
    if(abs(leftVelocity) < nullRange){  // Same on the other wheel
        leftVelocity = 0;
    }

  //The rightVelocity and leftVelocity ints now have a value from -255 to 255
  Serial.print("LeftSpd: ");
  Serial.print(abs(leftVelocity));
  Serial.print("\tRightSpd: ");
  Serial.println(abs(rightVelocity));
  // Output the signals to the motor driver hardware  
  digitalWrite(leftDir, sign(leftVelocity));    // Select the direction of the wheel based on whether the calculated wheel speed is positive or negative
  analogWrite(leftSpd, abs(leftVelocity));      // Set the PWM output, aka, set the speed

  digitalWrite(rightDir, !sign(rightVelocity));  // Same on the other wheel
  analogWrite(rightSpd, abs(rightVelocity));

}

void dump(char side){
  switch(side){
    case 'l':
      left.write(DUMP_VAL_LEFT);
      delay(2500);
      left.write(HOME_VAL_LEFT);
      break;
    case 'r':
      right.write(DUMP_VAL_RIGHT);
      delay(2500);
      right.write(HOME_VAL_RIGHT);
      break;
  }
}
