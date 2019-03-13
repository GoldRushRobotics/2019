#include <Wire.h>

#define V1 A0
#define V2 A1
#define V3 A2
#define V4 A3
#define DLFF1 3
#define DLFF2 4
#define DRFF1 5
#define DRFF2 6
#define FRFF1 7
#define FRFF2 8
#define FLFF1 9
#define FLFF2 10
#define RESET 11
#define TRIGGER 2
#define ERRORLED 13

#define debug 0

volatile bool error = false;

void setup() {
  if(debug) Serial.begin(115200);
  if(debug) Serial.println("A> Starting...");
  pinMode(V1, INPUT);
  pinMode(V2, INPUT);
  pinMode(V3, INPUT);
  pinMode(V4, INPUT);
  pinMode(DLFF1, INPUT);
  pinMode(DLFF2, INPUT);
  pinMode(DRFF1, INPUT);
  pinMode(DRFF2, INPUT);
  pinMode(FRFF1, INPUT);
  pinMode(FRFF2, INPUT);
  pinMode(FLFF1, INPUT);
  pinMode(FLFF2, INPUT);
  pinMode(RESET, OUTPUT);
  pinMode(TRIGGER, INPUT);
  pinMode(ERRORLED, OUTPUT);
  if(debug) Serial.println("A> Pins initialized.");

  digitalWrite(ERRORLED, LOW);
  digitalWrite(RESET, LOW);

  attachInterrupt(digitalPinToInterrupt(TRIGGER), checkPins, RISING);
  if(debug) Serial.println("A> Interrupt initialized.");
  
  
}

void loop() {
  writeVoltages();
  if(debug){
    writeErrors(digitalRead(DLFF1), digitalRead(DLFF2), "Driver Left");
    writeErrors(digitalRead(DRFF1), digitalRead(DRFF2), "Driver Right");
    writeErrors(digitalRead(FRFF1), digitalRead(FRFF2), "Feeder Right");
    writeErrors(digitalRead(FLFF1), digitalRead(FLFF2), "Feeder Left");
  }
  checkPins();
}

void writeVoltages(){
  int voltages[] = { analogRead(V1), analogRead(V2), analogRead(V3), analogRead(V4) };
  for (int i = 0; i < 4; i++) Serial.write(voltages[i]);
}
void writeErrors(int a, int b, String str){
  if (a == b){
    if (a == 1)
      Serial.println(str); //if both are high
  }else{
    if (a == 1)
      Serial.println(str); //a is high b is low
    else 
      Serial.println(str); //a is low b is high
  }
}

void checkPins () {
  error = (digitalRead(DLFF1)) || (digitalRead(DLFF2)) || (digitalRead(DRFF1)) || (digitalRead(DRFF2)) ||
          (digitalRead(FRFF1)) || (digitalRead(FRFF2)) || (digitalRead(FLFF1)) || (digitalRead(FLFF2));
  if(error) {
    digitalWrite(ERRORLED, HIGH);
    digitalWrite(RESET, HIGH);    
  }
}
