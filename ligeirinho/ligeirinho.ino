#include "Ligeirinho.h"
Ligeirinho robo;

#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_Sensor.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
#define OLED_RESET -1 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

#include <FluxGarage_RoboEyes.h>
roboEyes roboEyes; // create RoboEyes instance

void setup(){
  Serial.begin(9600);

  // Startup OLED Display
  // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3C or 0x3D
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }

  // Startup robo eyes
  roboEyes.begin(SCREEN_WIDTH, SCREEN_HEIGHT, 100); // screen-width, screen-height, max framerate

  // Define some automated eyes behaviour
  roboEyes.setAutoblinker(ON, 3, 2); // Start auto blinker animation cycle -> bool active, int interval, int variation -> turn on/off, set interval between each blink in full seconds, set range for random interval variation in full seconds
  roboEyes.setIdleMode(ON, 2, 2); // Start idle animation cycle (eyes looking in random directions) -> turn on/off, set interval between each eye repositioning in full seconds, set range for random time interval variation in full seconds

  // robo config
  robo.begin();
}

void update(int delay){
  float initial_time = millis();
  float final_time = delay;
  float current_time = initial_time;
  do {
    current_time = millis();
    roboEyes.update();
  } while((current_time-initial_time) < final_time);

  roboEyes.setMood(DEFAULT);
  roboEyes.setCuriosity(false);
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
    else if (comando.equals("RF")){
      robo.forward();
      delay(valor);
    }
    else if (comando.equals("RB")){
      robo.backwards();
      delay(valor);
    }
    else if(comando.equals("RCW")){
      robo.clockwise();
      robo.rotate(valor);
    }
    else if(comando.equals("RCCW")){
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
    else if (comando.equals("EA")){
      roboEyes.setMood(ANGRY);
      update(valor);
    }
    else if (comando.equals("EI")){
      roboEyes.setMood(DEFAULT);
      update(valor);
    }
    else if (msg.equals("EI0")){
      roboEyes.setMood(DEFAULT);
      roboEyes.setCuriosity(false);
    }
    else if (comando.equals("EH")){
      roboEyes.setMood(HAPPY);
      update(valor);
    }
    else if (comando.equals("ET")){
      roboEyes.setMood(TIRED);
      update(valor);
    }
    else if (comando.equals("EAC")){
      roboEyes.setMood(ANGRY);
      roboEyes.setCuriosity(true);
      update(valor);
    }
    else if (comando.equals("EIC")){
      roboEyes.setMood(DEFAULT);
      roboEyes.setCuriosity(true);
      update(valor);
    }
    else if (comando.equals("EHC")){
      roboEyes.setMood(HAPPY);
      roboEyes.setCuriosity(true);
      update(valor);
    }
    else if (comando.equals("ETC")){
      roboEyes.setMood(TIRED);
      roboEyes.setCuriosity(true);
      update(valor);
    }
    else if (comando.equals("EAL")){
      roboEyes.setMood(ANGRY);
      roboEyes.anim_laugh();
      update(1500);
    }
    else if (comando.equals("EIL")){
      roboEyes.setMood(DEFAULT);
      roboEyes.anim_laugh();
      update(1500);
    }
    else if (comando.equals("EHL")){
      roboEyes.setMood(HAPPY);
      roboEyes.anim_laugh();
      update(1500);
    }
    else if (comando.equals("ETL")){
      roboEyes.setMood(TIRED);
      roboEyes.anim_laugh();
      update(1500);
    }
    else if (comando.equals("EAS")){
      roboEyes.setMood(ANGRY);
      roboEyes.anim_confused();
      update(1500);
    }
    else if (comando.equals("EIS")){
      roboEyes.setMood(DEFAULT);
      roboEyes.anim_confused();
      update(1500);
    }
    else if (comando.equals("EHS")){
      roboEyes.setMood(HAPPY);
      roboEyes.anim_confused();
      update(1500);
    }
    else if (comando.equals("ETS")){
      roboEyes.setMood(TIRED);
      roboEyes.anim_confused();
      update(1500);
    }
  }
  //Serial.println("OLÁ");
  roboEyes.update();
}