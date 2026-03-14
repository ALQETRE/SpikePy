# SpikePy Documentation:
### About:
SpikePy is a robotics library made for PyBricks with the Spike Prime hub adding simple, precise, fast, relaible and customizable movement for two wheeled system. It achives this by using the onboard sensors in the hub and calculating corrections in real time for the best result.

<br>

This **Documentation** serves as a step by step guide on how to use SpikePy while explaining everithing along the way. If you want more direct or can't find something in this Documentation click [here](Documentation.md).

### [[Advanced Documentation]](Documentation.md)

<br>

## How to install:
place holder

## Code:

### Initalization:
Example:
```python
from spikepy import *

hub = PrimeHub()
left_port = Port.A
right_port = Port.E

wheel_rad = 29
axel_len = 96

left_wheel = Wheel(left_port, wheel_rad)
right_wheel = Wheel(right_port, wheel_rad)

bot = Robot(hub, left_wheel, right_wheel, axel_len)
```

<br>

#### 1. Importing:
The first thing is that you have to do is to import the library that you have installed.
```python
from spikepy import *
```
By doing this you will import everithing (*) from spikepy and that includes all pybrick functions so there is no need to import them.

#### 2. Setting up all parameters:
After importing the library we have to tell the code all our parameters.
```python
left_port = Port.A   # The left motor is pluged into port A
right_port = Port.E  # The right motor is pluged into port E

wheel_rad = 29  # The radius of the wheel is 29mm
axel_len = 96   # The distance between the wheels (from center to center) is 96mm
```

#### 3. Initilaze the robot:
When we have all the parameters, we can create the robot.
```python
hub = PrimeHub() # Create the hub with PyBricks

left_wheel = Wheel(left_port, wheel_rad)   # Create the wheels
right_wheel = Wheel(right_port, wheel_rad)

bot = Robot(hub, left_wheel, right_wheel, axel_len) # Combine everithing into a SpikePy robot
```