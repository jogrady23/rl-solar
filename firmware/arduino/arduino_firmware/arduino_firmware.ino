// Import servo library
#include <Servo.h>
#include <Adafruit_INA260.h>

// Create two separate Servo objects for each Servo
Servo servo_1;
Servo servo_2;

// Create ivp_1 and ivp_2 (will be added in the future with multiplexer)
// IVP = Current, voltage, power, a shorthand for the ina260 sensor
Adafruit_INA260 ivp_1 = Adafruit_INA260();

long start_ms;

const int servo_1_pin = 3;
const int servo_2_pin = 5;

int servo_1_position;
int servo_2_position;

float I_ivp_1;
float V_ivp_1;
float P_ivp_1;

const int SERIAL_BAUD_RATE = 9600;

// inbound commands
const int MOTOR_CONTROL = 1000;
const int SEND_MEASUREMENT = 2000;
const int RESET = 6666;

// outbound codes
const int ACKNOWLEDGE = 1111;
const int ERROR_MESSAGE = 9999;

int active_index;
int active_state;
bool send_data;

// MESSAGE PROCESSING
// --------------------

// constants for message processing
const char END_CHAR = '>';
const char MESSAGE_TERMINATOR = '\n';
const char DELIMITER = ',';

// variables for holding the final processed codes
const int CODE_ARRAY_SIZE = 5;
int code_array[CODE_ARRAY_SIZE];
int code_count;

// interim variables for loading in straight serial data
const int MAX_MESSAGE_CHARS = 32;
char message_array[MAX_MESSAGE_CHARS];
String serial_message;

// ===============================================
// FUNCTIONS
// ===============================================

// SERVO-CONTROL RELATED
// -----------------------------

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

void measure_motor_position() {
  servo_1_position = servo_1.read();
  servo_2_position = servo_2.read();
}

// Control a motor based on the code
void motor_control(int motor_1_degree, int motor_2_degree) {
  // write positions
  servo_1.write(degree_bounds(motor_1_degree));
  delay(300); // to avoid power spike
  servo_2.write(degree_bounds(motor_2_degree));
}

// POWER-MEASUREMENT RELATED
// -----------------------------

void power_measurement() {
  // placeholder
  I_ivp_1 = ivp_1.readCurrent()/1000; // convert to A
  V_ivp_1 = ivp_1.readBusVoltage()/1000; // convert to V
  P_ivp_1 = ivp_1.readPower()/1000; // convert to W
}

void state_update_sequence() {
  // take a measurement of motor positions
  measure_motor_position();
  // take power measurements (currently not used)
  power_measurement();
}

// INPUT REQUEST HANDLING
// -----------------------------

void process_input_request() {
  // motor control
  if (code_array[0] == 1000) {
    motor_control(code_array[1], code_array[2]);
    state_update_sequence();
    broadcast_state();
  }
  else if (code_array[0] == 2000) {
    state_update_sequence();
    broadcast_state();
  }
  else if (code_array[0] == 6666) {
    setup();
  }
  else {
    active_state = ERROR_MESSAGE;
  }
}


// CODE-PROCESSING RELATED
// -----------------------------

void clear_code_array() {
  for (int i = 0; i < CODE_ARRAY_SIZE; i++) {
    code_array[i] = 0;
  }
  active_index = 0;
}

// processes input string to extract codes
void process_input_message (String serial_message) {
  // find delimiters and endline
  int delim_index_array[10];
  int delim_count = 0;
  int end_index = 0;

  // convert the string to an array of character
  serial_message.toCharArray(message_array, MAX_MESSAGE_CHARS);

  // Identify the delimiter index locations and end character locations
  for (int i = 0; i < MAX_MESSAGE_CHARS; i++) {
    // find delimiter index
    if (message_array[i] == DELIMITER) {
      delim_index_array[delim_count] = i;
      delim_count += 1;
    }
    // find message end index
    if (message_array[i] == END_CHAR) {
      end_index = i;
    }
  }

  // If a valid input w/ end character, slice up array by delimiters to create an array of codes
  if (end_index != 0) {
    int loop_start_index = 0;
    int code_array_index = 0;
    // code count keeps track of number of codes
    code_count = 0;

    // first get the values between delimiters
    for (int i = 0; i < delim_count; i++) {
      String temp_string;
      for (int j = loop_start_index; j < delim_index_array[i]; j++) {
        temp_string += message_array[j];
      }
      // add to array
      code_array[code_array_index] = temp_string.toInt();
      code_count++;
      // increment store location in array
      code_array_index += 1;
      // increment start index
      loop_start_index = delim_index_array[i] + 1;
    }
    
    // then add the last characters between final delim and end character
    String temp_string;
    for (int j = loop_start_index; j < end_index; j++) {
      temp_string += message_array[j];
    }
    code_array[code_array_index] = temp_string.toInt();
    code_count++;
  }
}


// BROADCASTING RELATED
// -----------------------------

// sends out the Arduino's state
void broadcast_state() {
  float elapsed_s = (millis() - start_ms) / 1000.0;
  Serial.print(active_state);
  Serial.print(DELIMITER);
  Serial.print(elapsed_s, 3);
  Serial.print(DELIMITER);
  // servo positions
  Serial.print(servo_1_position);
  Serial.print(DELIMITER);
  Serial.print(servo_2_position);
  Serial.print(DELIMITER);
  // power measurements
  Serial.print(I_ivp_1, 3);
  Serial.print(DELIMITER);
  Serial.print(V_ivp_1, 3);
  Serial.print(DELIMITER);
  Serial.print(P_ivp_1, 3);
  // End message
  Serial.println(END_CHAR);
//  Serial.print(DELIMITER);
//  Serial.println(millis() - start);

  // reset clock
  start_ms = millis();
}

// for debugging
void broadcast_code_array() {
  // add protection for empty code
  if (code_count != 0) {
    // print all but last with delimiter
    for (int i = 0; i < code_count - 1; i++) {
      Serial.print(code_array[i]);
      Serial.print(DELIMITER);
    }
    // print last w/ newline
    Serial.println(code_array[code_count - 1]);
  }
}

// ===============================================
// SETUP AND LOOP
// ===============================================

void setup() {
  // Initialize Serial
  Serial.begin(SERIAL_BAUD_RATE);

  // Set to nominal state, change to error if anything arises
  active_state = ACKNOWLEDGE;
  
  // Configure motor pins
  servo_1.attach(servo_1_pin);
  servo_2.attach(servo_2_pin);
  
  // Initialize motor positions
  servo_1.write(0);
  servo_2.write(0);

  servo_1_position = servo_1.read();
  servo_2_position = servo_2.read();

  // Initialize INA260 sensor
  if (!ivp_1.begin()) {
    active_state = ERROR_MESSAGE;
  }
  // Take power measurement
  power_measurement();
  
  // tell Python that the program is initialized
  active_index = 0;
  send_data = false;
  clear_code_array();
  start_ms = millis();
}

void loop() {
  // Listen for new commands
  bool new_data = false;
  if (Serial.available() > 0) {
    serial_message = Serial.readStringUntil(MESSAGE_TERMINATOR);
    Serial.flush();
    new_data = true;
  }
  // If new command
  if (new_data == true) {
    process_input_message(serial_message);
    process_input_request();
  }
}
