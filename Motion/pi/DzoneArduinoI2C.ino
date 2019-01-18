#include <Wire.h>
#define SLAVE_ADDRESS 0x04
#define LED  13
int number = 0;
int count = 0;
int howMany[5];
void setup() {
  pinMode(LED, OUTPUT);
  Serial.begin(115200);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  //Wire.setClock(1000000);
  Serial.println("Ready!");
}
void loop() {
  delay(100);
}
void receiveData(int byteCount) {
  //Serial.print("receiveData");
  while (Wire.available()) {
    number = Wire.read();
    //Serial.print("\t");
    
    //Serial.print("\t");
    //Serial.print("data received: ");
    //Serial.println(number);
    //
    if (number == 1) {
      //Serial.println(" LED ON");
      digitalWrite(LED, HIGH);
    } else {
      //Serial.println(" LED OFF");
      digitalWrite(LED, LOW);
    }
    //
    
  }
  Wire.write(0x01);
  //Serial.println(count);
  count++;
}
void sendData() {
  Wire.write((const uint8_t*)& count, sizeof(count));
}
