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
int active_index;
int active_state;
bool send_data;

// message processing
const int CODE_ARRAY_SIZE = 3;
int code_array[CODE_ARRAY_SIZE];

const int MAX_MESSAGE_CHARS = 32;
char message_array[MAX_MESSAGE_CHARS];
String serial_message;

const char END_CHAR = '>';
const char MESSAGE_TERMINATOR = '\n';

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

void broadcast_code_array() {
  Serial.print(code_array[0]);
  Serial.print(DELIMITER);
  Serial.print(code_array[1]);
  Serial.print(DELIMITER);
  Serial.println(code_array[2]);
}

// populate code array from string input
void process_input_message (String serial_message) {
  // find delimiters and endline
  int delim_index_array[10];
  int delim_count = 0;
  int end_index;
  
  serial_message.toCharArray(message_array, MAX_MESSAGE_CHARS);
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
  // validate that at least message end found
  if (end_index != 0) {
    // break up input into distinct values and populate code_array
    
  }
  
}

void setup() {
  // Initialize active state
  active_state = UNAVAILABLE;
  
  // Initialize Serial
  Serial.begin(SERIAL_BAUD_RATE);
 

  // tell Python that the program is initialized
  active_state = ACKNOWLEDGE;
  active_listening = 0;
  active_index = 0;
  send_data = false;
}

void loop() {
  bool new_data = false;
  if (Serial.available() > 0) {
    serial_message = Serial.readStringUntil(MESSAGE_TERMINATOR);
    Serial.flush();
    new_data = true;
  }
  if (new_data == true) {
    serial_message.toCharArray(message_array, MAX_MESSAGE_CHARS);
//    Serial.print(message_array[0]);
//    Serial.print(DELIMITER);
//    Serial.println(message_array[1]);
    for (int i = 0; i < 20; i++) {
      if (i != 19) {
        Serial.print(message_array[i]);
        Serial.print(DELIMITER);
      }
      else {
        Serial.println(message_array[i]);
      }
    }
  }
}
