#include "gate.h"
#include "stepper_pot.h"

void setup() {
  gateSetup();
  binSetup();
}

void loop() {
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    // parse cmd, move servo, etc.
  }
  // whatever else Arduino needs to do continuously, if anything
}
