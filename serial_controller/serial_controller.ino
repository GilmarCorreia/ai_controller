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
  Serial.begin(9600); // Abrir porta serial

  pinMode(portaA1, OUTPUT); // sentido A
  pinMode(portaA2, OUTPUT); // sentido A
  pinMode(portaVelA, OUTPUT); // velocidade A

  pinMode(portaB1, OUTPUT); // sentido B
  pinMode(portaB2, OUTPUT); // sentido B
  pinMode(portaVelB, OUTPUT); // velocidade B

  pinMode(portaLED, OUTPUT); // porta LED
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

int anguloParaTempo(int angulo){
  float angVel_roda = ((180.0/180.0)*PI)/5.0;

  float rob_angVel = (raio_roda/raio_robo) * angVel_roda;

  float rob_rad = (angulo/180.0) * PI;
  return rob_rad/rob_angVel; 
}

void loop() {
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
      ligarMotores(valor);
    }
    else if (comando.equals("MF")){
      andarParaFrente();
      delay(valor);
    }
    else if (comando.equals("MB")){
      andarParaTras();
      delay(valor);
    }
    else if(comando.equals("CW")){
      girarHorario();
      float tempo = anguloParaTempo(valor);
      delay(tempo*1000);
    }
    else if(comando.equals("CCW")){
      girarAntihorario();
      float tempo = anguloParaTempo(valor);
      delay(tempo*1000);
    }
    else if(comando.equals("B")){
      piscarLED(valor);
    }
    else if(comando.equals("OFF")){
      desligarMotores();
    }
  }
}
