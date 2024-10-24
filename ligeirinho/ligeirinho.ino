#include "Ligeirinho.h"

Ligeirinho robo;

void setup(){
  Serial.begin(115200);
  robo.begin(); 

  //Serial.println("Robô PREPARADO!");
}

void loop(){
  delay(2000);
  robo.rotate(90.0); 
  delay(2000);
  //Serial.println(robo.readYaw());
}