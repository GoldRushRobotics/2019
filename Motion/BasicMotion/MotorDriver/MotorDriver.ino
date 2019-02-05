// R3: Jan 23, 2019: Basic functionality     -Greg Lewis
// R4: Jan 23, 2019: Smooth control         -Greg Lewis
// R5L Feb 2, 2019: WASD and Int implementation over serial   -Matt Wells

#define rightSpd 2  // PWM Magnitude
#define rightDir 3  // Digital direction
#define leftSpd 4
#define leftDir 5
#define feedGND 6
#define feedHOT 7

int speed = 0;     //0 = velocity, 1 = turn
int direction = 0;
int speedStep = 1;
int directionStep = 1;

void move(int velocity, int turn);  //Declare the main movement funtion

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

  while(Serial.available() <= 0);

  do {
    mode = Serial.read();
  } while(mode != 'w' && mode != 'a' && mode != 's' && mode != 'd' && mode != 'z');

  while(Serial.available() <= 0);

  val = Serial.parseInt();

  //Serial.println(mode);
  //Serial.println(val);
  
  switch(mode){
    case 'w': speed = val; direction = 0; break; //straight
    case 'a': direction = -val; break; //left
    case 's': speed = -val;  direction = 0; break; //backwards
    case 'd': direction = val; break; //right
    case 'z': speed = 0; direction = 0; break; //stop
  }
  
  move(speed, direction);
  
}

void move(int velocity, int turn){  //Velocity is the forward/back speed. Right is positive turn. left is negative
  int leftVelocity;
  int rightVelocity;
  
  //First, set both wheel values to the velocity (forward or backwards). The turn adjustments will be made next
  leftVelocity = velocity;    //The speed the left wheel turns
  rightVelocity = velocity;   //The speed the right wheel turns
  
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

  //Serial.print("leftVelocity: "); Serial.println(leftVelocity);
  //Serial.print("rightVelocity: "); Serial.println(rightVelocity);
  
  if(leftVelocity > 0){   
    //Serial.print("left Positive");
    digitalWrite(leftDir, HIGH); analogWrite(leftSpd, leftVelocity); //Left forwards
  }
  else if(leftVelocity < 0){
    digitalWrite(leftDir, LOW); analogWrite(leftSpd, leftVelocity * -1); //Left backwards
  }
  else{
    digitalWrite(leftDir, LOW); analogWrite(leftSpd, 0); //Left stop
  }
  
  if(rightVelocity > 0){
    //Serial.print("Right Positive");
    digitalWrite(rightDir, LOW); analogWrite(rightSpd, rightVelocity); //Right forwards
  }
  else if(rightVelocity < 0){
    digitalWrite(rightDir, HIGH); analogWrite(rightSpd, rightVelocity * -1); //Right backwards
  }
  else{
    digitalWrite(rightDir, LOW); analogWrite(rightSpd, 0); //Right stop
  }
}
