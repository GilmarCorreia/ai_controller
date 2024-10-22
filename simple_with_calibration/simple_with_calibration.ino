#include "MPU9250.h"

MPU9250 mpu;

int portaA1 = 2;
int portaA2 = 4;
int portaVelA = 3;

int portaB1 = 5;
int portaB2 = 7;
int portaVelB = 6;

int portaLED = 13;

int portaSensorDir = 0;
int portaSensorEsq = 1;

float raio_roda = (6.8/2.0)/100.0;
float raio_robo = (16.0/2.0)/100.0;

void setup() {
    Serial.begin(115200);
    Wire.begin();
    delay(2000);

    if (!mpu.setup(0x68)) {  // change to your own address
        while (1) {
            Serial.println("MPU connection failed. Please check your connection with `connection_check` example.");
            delay(5000);
        }
    }

    // calibrate anytime you want to
    Serial.println("Accel Gyro calibration will start in 5sec.");
    Serial.println("Please leave the device still on the flat plane.");
    mpu.verbose(true);
    delay(5000);
    mpu.calibrateAccelGyro();

    Serial.println("Mag calibration will start in 5sec.");
    Serial.println("Please Wave device in a figure eight until done.");
    delay(5000);
    mpu.calibrateMag();

    print_calibration();
    mpu.verbose(false);

    pinMode(portaA1, OUTPUT); // sentido A
    pinMode(portaA2, OUTPUT); // sentido A
    pinMode(portaVelA, OUTPUT); // velocidade A

    pinMode(portaB1, OUTPUT); // sentido B
    pinMode(portaB2, OUTPUT); // sentido B
    pinMode(portaVelB, OUTPUT); // velocidade B

    pinMode(portaLED, OUTPUT); // porta LED

    rotacionar(90);
}

void andarParaFrente(){
  digitalWrite(portaA1, HIGH);
  digitalWrite(portaA2, LOW);

  digitalWrite(portaB1, HIGH);
  digitalWrite(portaB2, LOW);
}

void andarParaTras(){
  digitalWrite(portaA1, LOW);
  digitalWrite(portaA2, HIGH);
  
  digitalWrite(portaB1, LOW);
  digitalWrite(portaB2, HIGH);
}

void girarAntihorario(){
  digitalWrite(portaA1, LOW);
  digitalWrite(portaA2, HIGH);
  
  digitalWrite(portaB1, HIGH);
  digitalWrite(portaB2, LOW);
}

void girarHorario(){
  digitalWrite(portaA1, HIGH);
  digitalWrite(portaA2, LOW);
  
  digitalWrite(portaB1, LOW);
  digitalWrite(portaB2, HIGH);
}

void ligarMotores(int vel){
  analogWrite(portaVelA, vel);
  analogWrite(portaVelB, vel);
}

void desligarMotores(){
  analogWrite(portaVelA, 0);
  analogWrite(portaVelB, 0);
}

void piscarLED(int tempo){
  digitalWrite(portaLED, HIGH);
  delay(tempo);
  digitalWrite(portaLED, LOW);
  delay(tempo);
}

int rotacionar(int angulo){
  float initial_angle = 0.0;
  float final_angle = angulo;
  float angleDiff = 0.0;

  float desired_error = 1.0;
  float error = 360.0;

  while (error > desired_error){
    if (mpu.update()){
      initial_angle = mpu.getYaw();

      if (initial_angle < 0){
        initial_angle = 360.0-initial_angle;
      }

      error = abs(final_angle - initial_angle);
      Serial.println(error);

      float initialVel = 0.0;
      float kp = 408.395*(1/3.1415);
      float vel = initialVel +  (kp * error);

      Serial.println(vel);

      girarHorario();
      ligarMotores(vel);
    }
  }
}

void loop(){

}
// void loop() {
//     if (mpu.update()) {
//         static uint32_t prev_ms = millis();
//         if (millis() > prev_ms + 25) {
//             print_roll_pitch_yaw();
//             prev_ms = millis();
//         }
//     }
// }

void print_roll_pitch_yaw() {
    Serial.print("Yaw, Pitch, Roll: ");
    Serial.print(mpu.getYaw(), 2);
    Serial.print(", ");
    Serial.print(mpu.getPitch(), 2);
    Serial.print(", ");
    Serial.println(mpu.getRoll(), 2);
}

void print_calibration() {
    Serial.println("< calibration parameters >");
    Serial.println("accel bias [g]: ");
    Serial.print(mpu.getAccBiasX() * 1000.f / (float)MPU9250::CALIB_ACCEL_SENSITIVITY);
    Serial.print(", ");
    Serial.print(mpu.getAccBiasY() * 1000.f / (float)MPU9250::CALIB_ACCEL_SENSITIVITY);
    Serial.print(", ");
    Serial.print(mpu.getAccBiasZ() * 1000.f / (float)MPU9250::CALIB_ACCEL_SENSITIVITY);
    Serial.println();
    Serial.println("gyro bias [deg/s]: ");
    Serial.print(mpu.getGyroBiasX() / (float)MPU9250::CALIB_GYRO_SENSITIVITY);
    Serial.print(", ");
    Serial.print(mpu.getGyroBiasY() / (float)MPU9250::CALIB_GYRO_SENSITIVITY);
    Serial.print(", ");
    Serial.print(mpu.getGyroBiasZ() / (float)MPU9250::CALIB_GYRO_SENSITIVITY);
    Serial.println();
    Serial.println("mag bias [mG]: ");
    Serial.print(mpu.getMagBiasX());
    Serial.print(", ");
    Serial.print(mpu.getMagBiasY());
    Serial.print(", ");
    Serial.print(mpu.getMagBiasZ());
    Serial.println();
    Serial.println("mag scale []: ");
    Serial.print(mpu.getMagScaleX());
    Serial.print(", ");
    Serial.print(mpu.getMagScaleY());
    Serial.print(", ");
    Serial.print(mpu.getMagScaleZ());
    Serial.println();
}
