#include <Stepper.h>
#include "stepper_pot.h"

const int rev = 2038;
Stepper stepper(rev, 8, 10, 9, 11);

void binSetup(){
  Serial.begin(9600);
}
