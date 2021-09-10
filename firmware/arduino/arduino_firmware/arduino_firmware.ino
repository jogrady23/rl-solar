// Import servo library
#include <Servo.h>

// Create two separate Servo objects for each Servo
Servo servo_1;
Servo servo_2;

const int servo_1_pin = 3;
const int servo_2_pin = 5;

int servo_1_position;
int servo_2_position;

const int SERIAL_BAUD_RATE = 9600;

// for internal state
const int MOTOR_CONTROL = 1000;
const int MOTOR_POSITIONS = 2000;
const int POWER_TOGGLE = 3000;
const int LISTEN_START = 4444;
const int LISTEN_COMPLETE = 5555;
const int RESET = 6666;

// Arduino responses
const int ACKNOWLEDGE = 1111;
const int UNAVAILABLE = 8888;
const int ERROR_MESSAGE = 9999;

const int STATUS_HEADER = 1;
const int DATA_HEADER = 2;
const char DELIMITER = ',';

int active_listening;
int active_index = 0;
int active_state;
bool send_data;

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

// sends out the Arduino's status
void broadcast_state(long start) {
  Serial.print(STATUS_HEADER);
  Serial.print(DELIMITER);
  Serial.print(active_state);
  Serial.print(DELIMITER);
  Serial.print(active_listening);
  Serial.print(DELIMITER);
  Serial.println(millis() - start);
}

// sends out data from the Arduino
void broadcast_data() {
  // Data header
  Serial.print(DATA_HEADER);
  Serial.print(DELIMITER);
  // motor 1 position,motor 2 position,solar power
  Serial.print(servo_1_position);
  Serial.print(DELIMITER);
  Serial.print(servo_2_position);
  // measure power
  // FIXME -- add power signal
}

void setup() {
  // Initialize active state
  active_state = UNAVAILABLE;
  
  // Initialize Serial
  Serial.begin(SERIAL_BAUD_RATE);
  
  // Configure motor pins
  servo_1.attach(servo_1_pin);
  servo_2.attach(servo_2_pin);
  
  // Initialize motor positions
  servo_1.write(0);
  servo_2.write(0);

  servo_1_position = servo_1.read();
  servo_2_position = servo_2.read();

  // tell Python that the program is initialized
  active_state = ACKNOWLEDGE;
  active_listening = 1;
  send_data = false;
}

void loop() {
  // Listen for serial inputs
  int code = 0;
  long start = millis();
  int initial_state = active_state;
  // If serial has bytes available, parse as int
  if (Serial.available() > 0) {
    code = Serial.parseInt();
    Serial.flush();

    // check for reset request
    if (code == RESET) {
      setup();
    }
    else {
      // if state is not available
      if (active_state != UNAVAILABLE) {
        
        // If not currently reading a message
        if (active_listening == 0) {
          
          // If requested to start listening
          if (code == LISTEN_START) {
            clear_code_array();
            active_listening = 1;
            active_state = ACKNOWLEDGE;
          }
          else {
            active_state = ERROR_MESSAGE;
          }
        }
        // Otherwise, assemble the char array until complete value arrives
        else {
          // if complete signal, stop listening and change state
          if (code == LISTEN_COMPLETE) {
            active_state = UNAVAILABLE;
            active_listening = 0;
          }
          // else, add to char array
          else {
            code_array[active_index] = code;
            active_state = ACKNOWLEDGE;
          }
        }
      }
    }
    // for any case, send the updated state message to Python
    broadcast_state(start);
  }
  

  // do whatever action is needed based on code array
  
  
  // Format message to broadcast at end of every loop
}
