#include "Ligeirinho.h"

Ligeirinho robo;
int initialSpeed = 255;

void setup(){
  Serial.begin(115200);
  robo.begin(); 
  //Serial.println("Robô PREPARADO!");
}

void loop(){
  if (Serial.available() > 0) {

    String msg = Serial.readStringUntil('\n');

    String comando = "";
    String num = "";

    for (int i = 0; i < msg.length(); i++){
      if(isDigit(msg[i])){
        num += msg[i];
      }
      else{
        comando += msg[i];
      }
    }

    int valor = num.toInt();

    Serial.println(comando);
    Serial.println(String(valor));
    
    if (comando.equals("ON")){
      initialSpeed = valor;
      robo.enginesSpeed(initialSpeed);
    }
    else if (comando.equals("MF")){
      robo.enginesSpeed(initialSpeed);
      robo.forward();
      delay(valor);
      robo.stop();
    }
    else if (comando.equals("MB")){
      robo.enginesSpeed(initialSpeed);
      robo.backwards();
      delay(valor);
      robo.stop();
    }
    else if(comando.equals("CW")){
      robo.clockwise();
      robo.rotate(valor);
    }
    else if(comando.equals("CCW")){
      robo.counterclockwise();
      robo.rotate(valor);
    }
    else if(comando.equals("BL")){
      robo.blink_led(valor);
    }
    else if(comando.equals("OFF")){
      robo.stop();
    }
    else if(comando.equals("LF")){
      // do{
      //   Serial.println(analogRead(robo.port_rightSensor));
      // }
      // while (Serial.available() <= 0);
      
      // Serial.readStringUntil('\n');

      // do{
      //   Serial.println(analogRead(robo.port_leftSensor));
      // }
      // while (Serial.available() <= 0);

      // Serial.readStringUntil('\n');

      robo.enginesSpeed(150);
      do{
        robo.line_follower(950);
      } while (Serial.available() <= 0);
      robo.stop();
    }
  }
}