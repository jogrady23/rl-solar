// Import servo library
#include <Servo.h>

// Create two separate Servo objects for each Servo
Servo servo_1;
Servo servo_2;

const int servo_1_pin = 3;
const int servo_2_pin = 5;

int servo_1_position;
int servo_2_position;

// for internal state
const int MOTOR_CONTROL = 1000;
const int MOTOR_POSITIONS = 2000;
const int POWER_TOGGLE = 3000;
const int LISTEN_START = 4444;
const int LISTEN_COMPLETE = 5555;
const int LISTEN_ACKNOWLEDGE = 1111;
const int AVAILABLE = 8888;
const int UNAVAILABLE = 8899;
const int ERROR_MESSAGE = 9999;

bool active_listening = false;
int active_index = 0;

bool send_power = false;

const int CODE_ARRAY_SIZE = 3;
int code_array[CODE_ARRAY_SIZE];

// Applies a safe 0-180 bound on any requested degree for writing to the Servo
int degree_bounds(int degree) {
  int safe_degree;
  if (degree > 180) {
    safe_degree = 180;
  }
  else if (degree < 0) {
    safe_degree = 0;
  }
  else {
    safe_degree = degree;
  }
  return safe_degree;
}

// Control a motor based on the code
void motor_control(char code, int degree) {
  // 1 = servo 1
  if (code=='1') {
    servo_1.write(degree_bounds(degree));
    delay(1000);
    servo_1_position = servo_1.read();
  }
  // 2 = servo 2
  if (code=='2') {
    servo_2.write(degree_bounds(degree));
    delay(1000);
    servo_2_position = servo_2.read();
  }
}

// Prints the motor position on Serial
void print_motor_position() {
  Serial.print(servo_1_position);
  Serial.print(',');
  Serial.println(servo_2_position);
}

void power_measurement(){
  void;
}

void process_input_request() {
  // motor control
  if (code_array[1] == 1000) {
    void;
  }
  // motor positions
  if (code_array[1] == 2000) {
    void;
  }
  // power measurements
  if (code_array[1] == 3000) {
    void;
  }
}

void clear_code_array() {
  for (int i = 0; i < CODE_ARRAY_SIZE; i++) {
    code_array[i] = 0;
  }
  active_index = 0;
}

void setup() {
  // Initialize Serial
  Serial.begin(9600);
  
  // Configure motor pins
  servo_1.attach(servo_1_pin);
  servo_2.attach(servo_2_pin);
  
  // Initialize motor positions
  servo_1.write(0);
  servo_2.write(0);

  servo_1_position = servo_1.read();
  servo_2_position = servo_2.read();

  // tell Python that the program is initialized
  Serial.println(AVAILABLE);
}

void loop() {
  // Listen for serial inputs
  int code = 0;
  
  // If serial has bytes available, parse as int
  if (Serial.available() > 0) {
    code = Serial.parseInt();
    
    // If not currently reading a message
    if (active_listening == false) {
      // If requested to start listening
      if (code == LISTEN_START) {
        clear_code_array();
        active_listening = true;
        Serial.println(LISTEN_ACKNOWLEDGE);
      }
      // If state is requested
    }
    // Otherwise, assemble the char array until 
    else {
      // if complete signal, stop listening and change state
      if (code == LISTEN_COMPLETE) {
        
      }
    }
  }
  
  
  // put your main code here, to run repeatedly:
  for (int i=0; i <= 180; i += 10) {
    servo_1.write(i);
    delay(200);
    servo_2.write(i);
    delay(1000);
  }
}
