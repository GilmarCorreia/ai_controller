#include "Ligeirinho.h"

Ligeirinho robo;

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

    //Serial.println(comando);
    //Serial.println(String(valor));

    if (comando.equals("ON")){
      robo.enginesSpeed(valor);
    }
    else if (comando.equals("MF")){
      robo.forward();
      delay(valor);
    }
    else if (comando.equals("MB")){
      robo.backwards();
      delay(valor);
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
  }
}