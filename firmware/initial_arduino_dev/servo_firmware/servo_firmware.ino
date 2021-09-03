// Import servo library
#include <Servo.h>

// Create two separate Servo objects for each Servo
Servo servo_1;
Servo servo_2;

int servo_1_pin = 3;
int servo_2_pin = 5;

void setup() {
  // put your setup code here, to run once:
  servo_1.attach(servo_1_pin);
  servo_2.attach(servo_2_pin);
  // write each to initial position
  servo_1.write(0);
  servo_2.write(0);
}

void loop() {
  // Listen for serial inputs

  // If serial available, send out data

  
  // put your main code here, to run repeatedly:
  for (int i=0; i <= 180; i += 10) {
    servo_1.write(i);
    delay(200);
    servo_2.write(i);
    delay(1000);
  }
}
