#include "Ligeirinho.h"

Ligeirinho::Ligeirinho() {
}

void Ligeirinho::begin(){
  //Serial.println("Configurando Ligeirinho");

  // Configurando o motor A
  pinMode(this->port_A1, OUTPUT); // sentido A
  pinMode(this->port_A2, OUTPUT); // sentido A
  pinMode(this->port_aSpeed, OUTPUT); // velocidade A

  // Configurando o motor B
  pinMode(this->port_B1, OUTPUT); // sentido B
  pinMode(this->port_B2, OUTPUT); // sentido B
  pinMode(this->port_bSpeed, OUTPUT); // velocidade B

  // Configurando porta do LED
  pinMode(this->port_LED, OUTPUT); // porta LED

  // Configurando IMU
  Wire.begin();
  delay(2000);
  if (!this->mpu.setup(0x68)) {  // endereço do mpu9250
    while (1) {
      Serial.println("MPU connection failed. Please check your connection with `connection_check` example.");
      delay(5000);
    }
  }

  // // calibrate anytime you want to
  // //Serial.println("Accel Gyro calibration will start in 5sec.");
  // //Serial.println("Please leave the device still on the flat plane.");
  // this->piscarLED(1000);
  // this->mpu.verbose(true);
  // delay(5000);
  // this->mpu.calibrateAccelGyro();

  // //Serial.println("Mag calibration will start in 5sec.");
  // //Serial.println("Please Wave device in a figure eight until done.");
  // this->piscarLED(1000);
  // this->piscarLED(1000);
  // delay(5000);
  // this->mpu.calibrateMag();

  // //this->print_calibration();
  // this->mpu.verbose(false);
}

void Ligeirinho::print_calibration() {
    Serial.println("< calibration parameters >");
    Serial.println("accel bias [g]: ");
    Serial.print(this->mpu.getAccBiasX() * 1000.f / (float)MPU9250::CALIB_ACCEL_SENSITIVITY);
    Serial.print(", ");
    Serial.print(this->mpu.getAccBiasY() * 1000.f / (float)MPU9250::CALIB_ACCEL_SENSITIVITY);
    Serial.print(", ");
    Serial.print(this->mpu.getAccBiasZ() * 1000.f / (float)MPU9250::CALIB_ACCEL_SENSITIVITY);
    Serial.println();
    Serial.println("gyro bias [deg/s]: ");
    Serial.print(this->mpu.getGyroBiasX() / (float)MPU9250::CALIB_GYRO_SENSITIVITY);
    Serial.print(", ");
    Serial.print(this->mpu.getGyroBiasY() / (float)MPU9250::CALIB_GYRO_SENSITIVITY);
    Serial.print(", ");
    Serial.print(this->mpu.getGyroBiasZ() / (float)MPU9250::CALIB_GYRO_SENSITIVITY);
    Serial.println();
    Serial.println("mag bias [mG]: ");
    Serial.print(this->mpu.getMagBiasX());
    Serial.print(", ");
    Serial.print(this->mpu.getMagBiasY());
    Serial.print(", ");
    Serial.print(this->mpu.getMagBiasZ());
    Serial.println();
    Serial.println("mag scale []: ");
    Serial.print(this->mpu.getMagScaleX());
    Serial.print(", ");
    Serial.print(this->mpu.getMagScaleY());
    Serial.print(", ");
    Serial.print(this->mpu.getMagScaleZ());
    Serial.println();
}

// Setters

// Getters
float Ligeirinho::readYaw(){
  if (this->mpu.update()) {
    float yaw = this->mpu.getYaw();
    float absoluteYaw = yaw;

    if (yaw < 0){
      absoluteYaw = 360.0 + yaw;
    }

    return absoluteYaw*(M_PI/180.0);
  }
  return 0.0;
}

// Controls
void Ligeirinho::forward(){
  digitalWrite(this->port_A1, HIGH);
  digitalWrite(this->port_A2, LOW);

  digitalWrite(this->port_B1, HIGH);
  digitalWrite(this->port_B2, LOW);
}

void Ligeirinho::backwards(){
  digitalWrite(this->port_A1, LOW);
  digitalWrite(this->port_A2, HIGH);
  
  digitalWrite(this->port_B1, LOW);
  digitalWrite(this->port_B2, HIGH);
}

void Ligeirinho::counterclockwise(){
  digitalWrite(this->port_A1, LOW);
  digitalWrite(this->port_A2, HIGH);
  
  digitalWrite(this->port_B1, HIGH);
  digitalWrite(this->port_B2, LOW);
}

void Ligeirinho::clockwise(){
  digitalWrite(this->port_A1, HIGH);
  digitalWrite(this->port_A2, LOW);
  
  digitalWrite(this->port_B1, LOW);
  digitalWrite(this->port_B2, HIGH);
}

void Ligeirinho::enginesSpeed(int speed){
  if (speed > 255)
      speed = 255;
  else if(speed<10)
      speed = 10;

  analogWrite(this->port_aSpeed, speed);
  analogWrite(this->port_bSpeed, speed);
}

void Ligeirinho::stop(){
  analogWrite(this->port_aSpeed, 0);
  analogWrite(this->port_bSpeed, 0);
}

void Ligeirinho::blink_led(int time){
  digitalWrite(this->port_LED, HIGH);
  delay(time/2);
  digitalWrite(this->port_LED, LOW);
  delay(time/2);
}

// Methods
float Ligeirinho::normalizeAngle(float angle){
  angle = fmod(angle,360.0);
  if(angle < 0)
      angle += 360.0;
  return angle * (M_PI/180.0);
}

void Ligeirinho::setSpeeds(float linear_speed, float angular_speed){
}

void Ligeirinho::rotate(float angle){
  float initial_time = ((float) millis())/1000.0;
  float final_time = initial_time;
  float total_time = 0;
  float currentAngle = 0;

  this->clockwise();
  this->enginesSpeed(225);
  do {
    if(this->mpu.update()){
      final_time = ((float) millis())/1000.0;
      float dt = final_time - initial_time;
      total_time += dt;
      currentAngle += abs(this->mpu.getGyroZ())*dt;
      //Serial.println(currentAngle); 

      initial_time = final_time;

      float erro = angle - currentAngle;
      this->enginesSpeed(255*(erro/angle));
    }
  } while ((currentAngle < angle) && (total_time < 1.5));

  this->stop();

}

void Ligeirinho::line_follower(int threshold){
  if(analogRead(this->port_rightSensor) < threshold && analogRead(this->port_leftSensor) < threshold){
    this->forward();
  }
  else if(analogRead(this->port_rightSensor) < threshold && analogRead(this->port_leftSensor) > threshold){
    this->counterclockwise();
  }
  else if(analogRead(this->port_rightSensor) > threshold && analogRead(this->port_leftSensor) < threshold){
    this->clockwise();
  }
  else{
    this->forward();
  }
}
// void Ligeirinho::rotate(float angle){
//   float initial_time = ((float) millis())/1000.0;
//   float final_time = initial_time;
//   float total_error = 0.0;
//   float theta_error = 1000.0;
//   float max_angular_speed = 255;//90.0 * (M_PI/180.0);
  
//   float theta_desired = 0.0;

//   float initial_angle = this->readYaw();
//   if (angle > 0)
//       theta_desired = this->normalizeAngle(initial_angle - angle);
//   else
//       theta_desired = this->normalizeAngle(initial_angle + angle);
      
//   float tr = 25.0;
//   float damping = 5;

//   float wn = 1.8/tr;
//   float Kp = 2*damping*wn;
//   float Ki = wn*wn;

//   while (theta_error > (0.5 * (M_PI/180.0))){
//       //Serial.print("initial angle: ");
//       //Serial.print(initial_angle);

//       //Serial.print(", desired yaw: ");
//       //Serial.print(theta_desired*(180.0/M_PI));

//       float current_yaw = this->readYaw();
//       //Serial.print(", current yaw: ");
//       //Serial.print(current_yaw*(180.0/M_PI));

//       float clockwise_distance = this->normalizeAngle((current_yaw - theta_desired)*(180.0/M_PI));
//       float counter_clockwise_distance = this->normalizeAngle((theta_desired - current_yaw)*(180.0/M_PI));

//       //Serial.print(", cw_dist: ");
//       //Serial.print(clockwise_distance*(180.0/M_PI));
//       //Serial.print(", ccw_dist: ");
//       //Serial.print(counter_clockwise_distance*(180.0/M_PI));

//       theta_error = min(clockwise_distance, counter_clockwise_distance);
//       //Serial.print(", error: ");
//       //Serial.print(theta_error*(180.0/M_PI));

//       final_time = ((float) millis())/1000.0;
//       float dt = final_time - initial_time;
//       total_error += theta_error * dt;
//       float control_signal = Kp * theta_error + (Ki * total_error);
//       //Serial.print(", control signal: ");
//       //Serial.print(control_signal);

//       float vel = 0.0;
//       if (clockwise_distance > counter_clockwise_distance){
//         this->clockwise();
//         vel = control_signal*max_angular_speed;
//       }
//       else{
//         this->counterclockwise();
//         vel = control_signal*max_angular_speed;
//       }

//       //Serial.print(", angular vel: ");
//       //Serial.println(abs(vel));

//       this->enginesSpeed(abs(vel));

//       initial_time = final_time;

//       //delay(1000);
//   }

//  this->desligarMotores();
//}