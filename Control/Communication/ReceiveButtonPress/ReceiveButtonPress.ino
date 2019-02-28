void setup() {
  
  Serial.begin(115200);

  bool waitForGo = false;

  do{
    waitForGo = Serial.read();
  } while(!waitForGo);
  
}

void loop() {
  // other main stuff

}
