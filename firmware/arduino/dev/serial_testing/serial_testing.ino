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

// MESSAGE PROCESSING
// --------------------

// constants for message processing
const char END_CHAR = '>';
const char MESSAGE_TERMINATOR = '\n';

// variables for holding the final processed codes
const int CODE_ARRAY_SIZE = 5;
int code_array[CODE_ARRAY_SIZE];
int code_count;

// interim variables for loading in straight serial data
const int MAX_MESSAGE_CHARS = 32;
char message_array[MAX_MESSAGE_CHARS];
String serial_message;


// FUNCTIONS
// -------------------

// broadcasts the processed codes that the Arduino just received
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
    process_input_message(serial_message);
    broadcast_code_array();
  }
}
