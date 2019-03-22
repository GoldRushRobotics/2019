#include <Servo.h>

#define LEFT_SERVO_PIN 9
#define RIGHT_SERVO_PIN 10

const int DUMP_VAL_LEFT = 10;
const int HOME_VAL_LEFT = 100;
const int DUMP_VAL_RIGHT = 140;
const int HOME_VAL_RIGHT = 50;

Servo left, right;

void setup() {
  Serial.begin(9600);
  left.attach(LEFT_SERVO_PIN);
  left.write(HOME_VAL_LEFT);
  right.attach(RIGHT_SERVO_PIN);
  right.write(HOME_VAL_RIGHT);

}

char mode, servoSide;

void loop() {
  
  while(Serial.available() <= 0);

  mode = Serial.read();

  if (mode == 'p'){
    while(Serial.available() <= 0);
    servoSide = Serial.read();
    dump(servoSide);
  }

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
