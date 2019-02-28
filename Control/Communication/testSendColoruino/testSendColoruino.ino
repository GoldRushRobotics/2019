#define COLORUINO //Pin Number

void setup() {
  Serial.begin(115200);

  int homeBaseVal = 0;

  do{
    homeBaseVal = Serial.parseInt();
  } while (!homeBaseVal);
  analogWrite(COLORUINO, homeBaseVal);
}

void loop() {
  //other main stuff
}
