#include <Servo.h>

#define LEFT_SERVO_PIN A1
#define RIGHT_SERVO_PIN A2

const int DUMP_VAL = 100;
const int HOME_VAL = 0;

Servo left, right;

void setup() {
  left.attach(LEFT_SERVO_PIN);
  right.attach(RIGHT_SERVO_PIN);

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
      left.write(DUMP_VAL);
      delay(2500);
      left.write(HOME_VAL);
      break;
    case 'r':
      right.write(DUMP_VAL);
      delay(2500);
      right.write(HOME_VAL);
      break;
  }
}
