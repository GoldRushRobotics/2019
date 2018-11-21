int i = 0;
void setup() {
  Serial.begin(9600);
}

void loop() {
  if (!i){
    while (micros() < 2000);
    Serial.write("1");
    i = 1;
  }
}
