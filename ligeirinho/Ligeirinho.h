#ifndef LIGEIRINHO_H
#define LIGEIRINHO_H

#include <Arduino.h>
#include "MPU9250.h"

class Ligeirinho {
public:
	Ligeirinho(){};

  void begin();
  
  // Getters
  //float readYaw();

  // Methods
  void print_calibration();
  void setSpeeds(float linear_speed, float angular_speed);
  void rotate(float angle);

  // Controls
  void forward();
  void backwards();
  void counterclockwise();
  void clockwise();
  void enginesSpeed(byte speed);
  void stop();
  void blink_led(int time);
  void line_follower(int threshold);

  // Sensores de refletância
  byte port_rightSensor = 0;
  byte port_leftSensor = 1;

private:
  // Motor A
	byte port_A1 = 2;
  byte port_A2 = 4;
  byte port_aSpeed = 3;
  byte port_encoderA1 = 8;
  byte port_encoderA2 = 9;

  // Motor B
  byte port_B1 = 5;
  byte port_B2 = 7;
  byte port_bSpeed = 6;
  byte port_encoderB1 = 10;
  byte port_encoderB2 = 11;

  // LED
  byte port_LED = 13;

  // // Sensor IMU
  // MPU9250 mpu;

  // Propriedades do robô
  //float wheel_radius = (6.5/2.0)/100.0;
  //float wheel_track = (16.0/2.0)/100.0;

  // Methods
  float normalizeAngle(float angle);
};
#endif