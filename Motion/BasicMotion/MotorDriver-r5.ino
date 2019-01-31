
// R3: Jan 23, 2019: Basic functionality     -Greg Lewis
// R4: Jan 23, 2019: Smooth control         -Greg Lewis

#define rightSpd 3  // PWM Magnitude
#define rightDir 2  // Digital direction
#define leftSpd 5
#define leftDir 4
#define feedGND 6
#define feedHOT 7

int speed = 128;     //0 = velocity, 1 = turn
int direction = 128;
int speedStep = 12;
int directionStep = 12;
char vl = 0;        //Shortcut for velocity
char tn = 1;        //Shortcut for turn

void move(int velocity, int turn);  //Declare the main movement funtion
void moveChar(int velocityChar, int turnChar);
void halt();
void m();

void setup(void)
{
  Serial.begin(115200);
  Serial.println("setup");
  pinMode(rightSpd, OUTPUT);
  pinMode(rightDir, OUTPUT);
  pinMode(leftSpd, OUTPUT);
  pinMode(leftDir, OUTPUT);
  pinMode(feedGND, OUTPUT);
  pinMode(feedHOT, OUTPUT);
  digitalWrite(feedHOT, HIGH);
  digitalWrite(feedGND, LOW);
}



void loop(void){
  
  int val = 0;
  char mode = 0;

  do {
    mode = Serial.read();
  } while(mode != 's' && mode != 't');

    
  Serial.println(mode);
  Serial.read();
  Serial.read();

  do {
    val = Serial.read();
  } while(val < 65 && val > 122);

    
  if(mode == 's'){
    speed = val;
  }else if(mode == 't'){
    direction = val;
  }
  Serial.print("val: "); Serial.println(val);
  Serial.print("spd: "); Serial.println(speed);
  Serial.print("dir: "); Serial.println(direction);
  moveChar(speed, direction);
  
}

void moveChar(int velocityChar, int turnChar){   //Takes in values from 0 to 255 for velocity and turn
  int convertedVel = map(velocityChar, 65, 172, -255, 255);  //Stretch a char's range to int for the function
  int convertedTurn = map(turnChar, 65, 172, -255, 255);
  move(convertedVel, convertedTurn);
}

void move(int velocity, int turn){  //Velocity is the forward/back speed. Right is positive turn. left is negative
  int leftVelocity;
  int rightVelocity;


  
  //First, set both wheel values to the velocity (forward or backwards). The turn adjustments will be made next
  leftVelocity = velocity;    //The speed the left wheel turns
  rightVelocity = velocity;   //The speed the right wheel turns

  
  //##TO DO: There is currently protection for values over 255 but not values under -255
  if(turn > 0){         //If we are turning right
    leftVelocity += turn;   //Adjust speed of left wheel so it turns right
    
    if(leftVelocity > 255){   //If the left wheel can't turn any faster, slow the right one to increase turning
      rightVelocity -= leftVelocity - 255;  //Subtract the extra from the right wheel
      leftVelocity = 255;   //Left velocity is set to the maximum
    }
  }
    else if(turn < 0){        //If we are turning left
    rightVelocity -= turn;      //Adjust speed of right wheel so it turns left
    
    if(rightVelocity > 255){    //If the right wheel can't turn any faster, slow the left one to increase turning
      leftVelocity -= rightVelocity - 255;  //Subtract the extra from the right wheel
      rightVelocity = 255;    //Right velocity is set to the maximum
    }
  }
  
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

void halt(){
  speed = 128;
  direction = 128;
  moveChar(speed, direction);
}
void m(){
  moveChar(speed, direction);
  delay(80);
}
