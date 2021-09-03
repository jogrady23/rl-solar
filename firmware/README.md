# Arudino Python Interface
This page documents the expected interface between the Python RL agent 
and the Arduino firmware operating the motors / sending power measurements

## Control Codes
This system utilizes a call-and-response type approach to ensure motor commands are 
successfully sent from Python and received by the Arduino.

The Python agent has the following classes of commands to Arduino:
* Motor control
    * Move motor 1
    * Move motor 2
* Motor positions
    * Get motor 1 position
    * Get motor 2 position
* Power measurement
    * Start power measurement broadcast
    * Stop power measurement broadcast

To simplify things on the Arduino end, we can use a distinct code for each of these actions, 
such that Arduino listens for the code and the subsequent value to understand what action to 
take.

### Motor Control

* `1000`: Tells the Arduino that motor control is desired
    * `1`: Tells the Arduino that motor 1 is the desired motor to control
    * `2`: Tell the Arduino that motor 2 is the desired motor to control 
    
After these codes are received, the desired degree will be broadcasted by Python to 
Arduino (value between 0 and 180).

### Motor Positions

* `2000`: Tells the Arduino that the agent is requesting motor positions
    * Arduino will send `<motor 1 position>,<motor 2 position>` to Python
    
### Power Measurement
* `3000`: Tells the Arduino the agent wants to toggle power measurement
    * `1`: Tells the Arduino to start broadcasting power measurement
    * `2`: Tells the Arduino to stop broadcasting power measurement
    
### End of Command
* `4444`: Tells the Arduino that it can stop listening for new commands

### Arduino Acknowledge
* `1111`: The Arduino will broadcast this in response to a successfully received 
message from Python
  

    