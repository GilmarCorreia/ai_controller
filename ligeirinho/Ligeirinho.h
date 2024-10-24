#ifndef LIGEIRINHO_H
#define LIGEIRINHO_H
#include <Arduino.h>
#include "MPU9250.h"

class Ligeirinho {
public:
	Ligeirinho();

  void begin();

  // Getters
  float readYaw();

  // Methods
  void print_calibration();
  void setSpeeds(float linear_speed, float angular_speed);
  void rotate(float angle);
private:
  // Motor A
	int port_A1 = 2;
  int port_A2 = 4;
  int port_aSpeed = 3;

  // Motor B
  int port_B1 = 5;
  int port_B2 = 7;
  int port_bSpeed = 6;

  // LED
  int port_LED = 13;

  // Sensores de refletância
  int port_rightSensor = 0;
  int port_leftSensor = 1;

  // Sensor IMU
  MPU9250 mpu;

  // Propriedades do robô
  float wheel_radius = (6.8/2.0)/100.0;
  float wheel_track = (16.0/2.0)/100.0;

  // Controls
  void andarParaFrente();
  void andarParaTras();
  void girarAntihorario();
  void girarHorario();
  void ligarMotores(int vel);
  void desligarMotores();
  void piscarLED(int tempo);

  // Methods
  float normalizeAngle(float angle);
};
#endif