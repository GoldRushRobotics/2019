#define rightSpd 5
#define rightDir 4
#define leftSpd 6
#define leftDir 7

void setup() {
  Serial.begin(9600);
  /*
  pinMode(rightSpd, OUTPUT);
  pinMode(rightDir, OUTPUT);
  pinMode(leftSpd, OUTPUT);
  pinMode(leftDir, OUTPUT);
  analogWrite(rightSpd, 0);
  digitalWrite(rightDir, 0);
  analogWrite(leftSpd, 0);
  digitalWrite(leftDir, 0);
  */
}

void loop() {
  // put your main code here, to run repeatedly:
  for (int i = 18; i <= 19; i++){
    pinMode(i, OUTPUT);
    Serial.println(i);
    analogWrite(i, 0);
    analogWrite(i, 150);
    delay(2000);
    analogWrite(i, 0);
    delay(2000);
  }
}
