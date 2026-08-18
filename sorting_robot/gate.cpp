#include <Servo.h>
#include "gate.h"

Servo servo;
const int servoPin = 7;

void gateSetup(){
  servo.attach(servoPin);
}

void openGate(){
  for (int pos = 0; pos <= 180; pos++){
    servo.write(pos);
    delay(15);
  }
}

void closeGate(){
  for (int pos = 180; pos >= 0; pos--){
    servo.write(pos);
    delay(15);
  }
}
