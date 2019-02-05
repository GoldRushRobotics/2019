/*
  I2C Pinouts
  SDA -> A4
  SCL -> A5
*/

//Import the library required
#include <Wire.h>

//Slave Address for the Communication
#define SLAVE_ADDRESS 0x08

char number[50];
int state = 0;

//Code Initialization
void setup() {
  // initialize i2c as slave
  Serial.begin(9600);
  Serial.println("Startup");
  Wire.begin(SLAVE_ADDRESS);
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  //  Wire.onRequest(sendData);
}

void loop() {
  delay(100);
} // end loop

// callback for received data
void receiveData(int byteCount) {
  Serial.println("Received Message!");
  int i = 0;
  while (Wire.available()) {
    number[i] = Wire.read();
    Serial.print(number[i]);
    i++;
  }
  number[i] = '\0';
  Serial.println();
}  // end while

//End of the program
