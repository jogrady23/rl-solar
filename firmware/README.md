# Arudino Python Interface
This page documents the expected interface between the Python RL agent 
and the Arduino firmware operating the motors / sending power measurements

During each loop, the Arduino will check for any commands or state changes. At the end of each loop, Arudino will 
broadcast its data sequence.

## Communication to Arduino

In any given message, the arduino will receive a comma-delimited string with the following format:

* code
* values related to code (one to many)
* end character (>)
* newline character (not included in snippets below)

### Motor Control

* `1000`: Tells the Arduino that motor control is desired
  * This code is followed by two values, the desired angles for motor 1 and motor 2 respectively
    
### Special commands
* `6666`: Tells the Arduino to reset (used if Arduino is not sending expected responses)

## Communication from Arduino

At the end of each loop(), the Arduino will broadcast (as a comma-delimited string):

* internal state code
* time since last message (seconds)
* motor 1 position
* motor 2 position
* current sensor 1 (A)
* voltage sensor 1 (V)
* power sensor 1 (W)
* current sensor 2 (A)
* voltage sensor 2 (V)
* power sensor 2 (W)

### Arduino Internal States
* `1111`: The Arduino will broadcast this in response to a successfully received 
message from Python
* `9999`: Indicates the Arduino is requesting a sequence re-start / invalid data / some error

---

## Examples

### Nominal Case

**To Arduino**

In a nominal case, the Python agent may send something like:

`1000,24,167>`

which would indicate motor control, motor 1 = 24°, motor 2 = 167°

**From Arduino**

The Arduino would then respond something like:

`1111,0.823,24,167,0.34,5,1.7,-0.5,5,-2.5>`

### Non-Nominal Case

Now, if the Arduino had some issue such that it could not complete the command, then it may send back:

`9999>`

to which the Python agent would attempt a reset, sending:

`6666>`

to which the Arduino should respond:

`1111,....>`

after it has successfully reset itself.


  

    