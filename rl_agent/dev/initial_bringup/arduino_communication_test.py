import pandas as pd
import time
import serial

# function to change motor to angle

# function to "move" panel by coordinating both motors

def readSerialLine(ser):
    """
    Reads data from Serial (from Arduino)

    Args:
        ser(byte): Serial line from Arduino
    Returns:
        (str): The output of the line
    """
    line = ser.readline()
    line = line.decode("utf-8")
    data_line = line
    line_output = data_line.strip()
    return line_output


if __name__ == '__main__':
    # Initialize serial port
    serial_port = '/dev/cu.usbmodem14201'
    baud_rate = 9600
    arduino = serial.Serial(port=serial_port, baudrate=baud_rate, timeout=1)
    time.sleep(2)

    # Tell the Arduino to take the initial OCV measurement
    while arduino.in_waiting() < 0:
        time.sleep(0.1)
    arduinoData = readSerialLine(arduino)
    initialVoltage = float(arduinoData) / 2 # divide by 2 since SoC(OCV) function is for 1 cell's OCV