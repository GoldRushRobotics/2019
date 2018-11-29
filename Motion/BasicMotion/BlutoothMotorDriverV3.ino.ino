//Conventions in this code:
//General comment
//##change to be made##
//??question??

#include <Wire.h>

#define rightSpd 3
#define rightDir 2
#define leftSpd 5
#define leftDir 4
#define feedGND 6
#define feedHOT 7

int currentMovement[4];     //0 = velocity, 1 = turn
char vl = 2;        //Shortcut for velocity
char tn = 3;        //Shortcut for turn

void move(int velocity, int turn);  //Declare the main movement funtion
void derement();          //Have the speed and turn slowly return to 0

void setup(void)
{
  Serial.begin(9600);     //##Change Code And Wiring To Serial1##
  Wire.begin(8);                // join i2c bus with address #8
  Wire.onReceive(receiveEvent); // register event
  Serial.println("setup");
  pinMode(rightSpd, OUTPUT);
  pinMode(rightDir, OUTPUT);
  pinMode(leftSpd, OUTPUT);
  pinMode(leftDir, OUTPUT);
  pinMode(feedGND, OUTPUT);
  pinMode(feedHOT, OUTPUT);
  digitalWrite(feedHOT, HIGH);    //?? What do these do? Surely we aren't powering the motors from the data pins ??
  digitalWrite(feedGND, LOW);

  //Test
  /*
  move(100, 0);
  delay(1000);
  move(-100, 0);
  delay(1000);
  move(0, -50);
  delay(1000);
  move(0, 50);
  delay(1000);
  move(0, 0);
  */
}
int spdStep = 50;   //The amount to increment speed on keypress
int turnStep = 50;  //Same for turn
int fadeStep = 1; //IMPORTANT: this value should be one for the time being. A higher number could make the bot oscillate between left/right or fwd/bkw
/*
void loop(void)
{
  if (Serial.available()) {     //If there is serial data available, run this loop. If not, carry on. Using an if() rather than a while() allows other code to run while there is no serial input
    char val = Serial.read();
    
    switch(val) // Perform an action depending on the command
    {
      case '119'://Move Forward
      case 'W':
      currentMovement[vl] += spdStep;
        break;
      case '115'://Move Backwards
      case 'S':
      currentMovement[vl] -= spdStep;
        break;
      case '97'://Turn Left
      case 'A':
      currentMovement[tn] -= turnStep;
        break;
      case '100'://Turn Right
      case 'D':
      currentMovement[tn] += turnStep;
        break;
        case 'f'://Turn Right
      case 'F':
        currentMovement[tn] += turnStep;
        break;
      default:
        //stop1();
        //delay(20);
        break;
    }
  }
  decrement();    //Slowly decrease the velocity and turn values each cycle
  delay(0);     //If decrement is too fast, a delay on the loop can slow it down. ##Change to function of millis() to wait without delay()##
  
  move(currentMovement[vl], currentMovement[tn]); //Update the motor controllers with their new values
}
*/
void loop(void){
  delay(10);
  //decrement();
  //move(currentMovement[0], currentMovement[1]);
  
  
}
// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany) {
  char data[howMany + 2];
  int i = -1;
  int stopFlag = 0;
  Serial.println("INPUT");
  while (1 < Wire.available()) { // loop through all but the last
    int c = Wire.read(); // receive byte as a character
    Serial.print(c);         // print the character
    Serial.print("\t");
    data[i] = c;
    if(i == 0){   //c == 102){
      stopFlag = 1;
    }
    currentMovement[i] = c;
    i++;
  }
  int x = Wire.read();    // receive byte as an integer
  Serial.println(x);         // print the integer
  currentMovement[vl] = data[1];
  currentMovement[tn] = data[2];
  //moveChar(data[1], data[2]);
  
//  if(stopFlag != 0){
//    Serial.println("STOP DAMNIT");
////    move(0, 0);
//    currentMovement[vl] = 0;
//    currentMovement[tn] = 0;
//    }
}

void moveChar(int velocityChar, int turnChar){   //Takes in values from 0 to 255 for velocity and turn
  currentMovement[vl] = map(velocityChar, 0, 255, -255, 255);  //Stretch a char's range to int for the function
  currentMovement[tn] = map(turnChar, 0, 255, -255, 255);
  move(currentMovement[vl], currentMovement[tn]);
}

void move(int velocity, int turn){  //Velocity is the forward/back speed. Right is positive turn. left is negative
  int leftVelocity;
  int rightVelocity;
  //First, set both wheel values to the velocity (forward or backwards). The turn adjustments will be made next
  leftVelocity = velocity;    //The speed the left wheel turns
  rightVelocity = velocity;   //The speed the right wheel turns

  Serial.print(leftVelocity);
  Serial.print("\t");
  Serial.print(rightVelocity);
  Serial.print("\t\t");

  /*
  //##TO DO: There is currently protection for values over 255 but not values under -255
  if(turn > 0){         //If we are turning right
    leftVelocity += turn;   //Adjust speed of left wheel so it turns right
    
    if(leftVelocity > 255){   //If the left wheel can't turn any faster, slow the right one to increase turning
      rightVelocity -= leftVelocity - 255;  //Subtract the extra from the right wheel
      leftVelocity = 255;   //Left velocity is set to the maximum
    }

    if(leftVelocity < -255){    //If the right wheel can't turn any faster, slow the left one to increase turning
      rightVelocity += leftVelocity + 255;  //Subtract the extra from the right wheel
      leftVelocity = -255;    //Right velocity is set to the maximum
    }
  }
    else if(turn < 0){        //If we are turning left
    rightVelocity += turn;      //Adjust speed of right wheel so it turns left
    
    if(rightVelocity > 255){    //If the right wheel can't turn any faster, slow the left one to increase turning
      leftVelocity -= rightVelocity - 255;  //Subtract the extra from the right wheel
      rightVelocity = 255;    //Right velocity is set to the maximum
    }

    if(rightVelocity < -255){    //If the right wheel can't turn any faster, slow the left one to increase turning
      leftVelocity += rightVelocity + 255;  //Subtract the extra from the right wheel
      rightVelocity = -255;    //Right velocity is set to the maximum
    }
  }
  */

  Serial.print(leftVelocity);
  Serial.print("\t");
  Serial.print(rightVelocity);
  Serial.println();
  
  //The rightVelocity and leftVelocity ints now have a value from -255 to 255
  
  if(leftVelocity > 0){   
    digitalWrite(leftDir, HIGH); analogWrite(leftSpd, leftVelocity); //Left forwards
  }
  else if(leftVelocity < 0){
    digitalWrite(leftDir, LOW); analogWrite(leftSpd, leftVelocity * -1); //Left backwards
  }
  else{
    digitalWrite(leftDir, LOW); analogWrite(leftSpd, 0); //Left stop
  }
  
  if(rightVelocity > 0){
    digitalWrite(rightDir, LOW); analogWrite(rightSpd, rightVelocity); //Right forwards
  }
  else if(rightVelocity < 0){
    digitalWrite(rightDir, HIGH); analogWrite(rightSpd, rightVelocity * -1); //Right backwards
  }
  else{
    digitalWrite(rightDir, LOW); analogWrite(rightSpd, 0); //Right stop
  }
  
}

void decrement(){
  if(currentMovement[vl] > 0){
    currentMovement[vl] -= fadeStep;
  }
  if(currentMovement[vl] < 0){
    currentMovement[vl] += fadeStep;
  }
  if(currentMovement[tn] > 0){
    currentMovement[tn] -= fadeStep;
  }
  if(currentMovement[tn] < 0){
    currentMovement[tn] += fadeStep;
  }

}
/*
 * The old motor drive code
void stop1() //Stop
{
  analogWrite(leftSpd, 0); analogWrite(rightSpd, 0);
}
void forward(int spd) //Drive forward
{
  digitalWrite(leftDir, HIGH); analogWrite(leftSpd, spd); //Left forwards
  digitalWrite(rightDir, LOW); analogWrite(rightSpd, spd); //Right forwards
}
void backward(int spd) //Drive backwards
{
  digitalWrite(leftDir, LOW); analogWrite(leftSpd, spd); //Left backwards
  digitalWrite(rightDir, HIGH); analogWrite(rightSpd, spd); //Right backwards
}
void left(int spd) //Drive left
{
  digitalWrite(leftDir, LOW); analogWrite(leftSpd, sped); //Left backwards
  digitalWrite(rightDir, LOW); analogWrite(rightSpd, sped); //Right forwards
}
void right(int spd) //Drive right
  digitalWrite(leftDir, HIGH); analogWrite(leftSpd, sped); //Left forwards
  digitalWrite(rightDir, HIGH); analogWrite(rightSpd, sped); //Right backwards
}
*/
