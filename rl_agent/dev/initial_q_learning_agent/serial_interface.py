import serial
import time
import random
import pandas as pd

import plotly.express as px
import plotly.io as pio

# Request codes
MOTOR_CONTROL = 1000
STATE_REQUEST = 2000
RESET_CODE = 6666

# Response codes
NOMINAL = 1111
ERROR = 9999

# Constants for communication
END_CHAR = '>'
MESSAGE_TERMINATOR = '\n'
DELIMITER = ','
RESPONSE_TIMEOUT = 3
ABORT_TIMEOUT = 5


def read_serial_line(serial_device: serial.Serial, print_message=True):
    """
       Reads data from Serial (from Arduino) with a safe check for end char

       Args:
           serial_device (serial.Serial): The Serial device
       Returns:
           (str): The output of the line, or None if invalid message
    """
    data_line = serial_device.readline().decode().strip()
    if END_CHAR in data_line:
        data_list = data_line.replace(END_CHAR, '').split(DELIMITER)
    else:
        data_list = None
    if print_message:
        print('Reading message: ' + str(data_list))
    return data_list

def write_serial_line(serial_device: serial.Serial, code_array, write_timeout=3, print_message=True):
    """
    Args:
        serial_device (serial.Serial): The Serial device
        code_array (list): The sequence of codes/values to send to Arduino

    Returns:
        (bool): True for successful write, False for timeout

    """
    message = ','.join([str(x) for x in code_array]) + END_CHAR + MESSAGE_TERMINATOR

    # Track write time or timeout
    write_success = True
    write_start = time.time()
    serial_device.write(str(message).encode())

    # Attempt to write message
    if print_message:
        print('Writing serial message: ' + str(code_array))
    while (serial_device.out_waiting > 0) and (time.time() - write_start < write_timeout):
        time.sleep(0.05)
    if (time.time() - write_start > write_timeout) and (serial_device.out_waiting > 0):
        write_success = False

    # Reset buffer
    serial_device.reset_output_buffer()

    return write_success

def listen_for_serial(serial_device: serial.Serial):
    # returns message, abort tuple
    abort = False
    message = None
    wait_start = time.time()
    while arduino.in_waiting <= 0 and time.time() - wait_start < RESPONSE_TIMEOUT:
        time.sleep(0.001)
    # Case for successful response
    if arduino.in_waiting > 0:
        message = map_message_to_dict(time.time(), read_serial_line(arduino, print_message=False))
    # If no response, send a reset request
    else:
        print('WARNING: Arduino unresponsive, requesting reset...')
        write_serial_line(arduino, [RESET_CODE])
        # Verify the reset
        wait_start = time.time()
        while arduino.in_waiting <= 0 and time.time() - wait_start < RESPONSE_TIMEOUT:
            time.sleep(0.005)
        if arduino.in_waiting > 0:
            print('SUCCESS: Arduino reset successfully.')
            message = map_message_to_dict(time.time(), read_serial_line(arduino, print_message=False))
        else:
            print('FATAL ERROR: Arduino unresponsive to reset.')
            abort = True
    return message, abort

def initialize_serial(serial_port='/dev/cu.usbmodem14101', baud_rate=9600, timeout=2):
    serial_device = serial.Serial(port=serial_port, baudrate=baud_rate, timeout=timeout)
    serial_device.flush()
    time.sleep(2)
    return serial_device

def map_message_to_dict(timestamp, input_message):
    final_dict = {}
    if input_message is not None:
        final_dict = {
            'timestamp': timestamp,
            'state': input_message[0],
            'arduino_duration': input_message[1],
            'motor_1_position': input_message[2],
            'motor_2_position': input_message[3],
            'I_ivp_1': input_message[4],
            'V_ivp_1': input_message[5],
            'P_ivp_1': input_message[6]
        }
    return final_dict