void setup() {
  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
  pinMode(13,OUTPUT);
}

void loop() {
  // send data only when you receive data:
  if (Serial.available() > 0) {

    // read the incoming byte:
    String incomingMsg = Serial.readStringUntil('\n');

    if (incomingMsg.equals("MF5")){
      digitalWrite(13, HIGH);
      delay(5000);
    }

    if (incomingMsg.equals("MF6")){
      digitalWrite(13, LOW);
      delay(1000);
    }

  }
}