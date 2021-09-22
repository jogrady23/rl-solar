# Arudino Python Interface
This page documents the expected interface between the Python RL agent 
and the Arduino firmware operating the motors / sending power measurements

## Control Codes
This system utilizes a call-and-response type approach to ensure motor commands are 
successfully sent from Python and received by the Arduino.

### Arduino Recieves

#### Motor Control

* `1000`: Tells the Arduino that motor control is desired
  * After these codes are received, the desired degree will be broadcasted by Python to 
Arduino (value between 0 and 180)
  * This broadcasts an array of [motor 1, motor 2] position

#### Measurement Broadcast
* `2000`: Tells the Arduino a measurement start/stop request is inbound
  * `0`: Stop measurement broadcast
  * `1`: Start measurement broadcast
    
#### Start/End of Command
* `4444`: Tells the Arduino to start listening for a new command
* `5555`: Tells the Arduino that it can stop listening for new commands
* `6666`: Tells the Arduino to reset

### Arduino Sends

#### Arduino Acknowledge
* `1111`: The Arduino will broadcast this in response to a successfully received 
message from Python
* `8888`: Indicates the Arduino is completing an action and is not ready for a message
* `9999`: Indicates the Arduino is requesting a sequence re-start / invalid data
  

    