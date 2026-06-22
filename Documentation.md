# About SpikePy:
SpikePy is a robotics library made for PyBricks with the SPIKE Prime hub, adding simple, precise, fast, reliable, and customizable movement for two-wheeled systems. It achieves this by using the onboard sensors in the hub and calculating corrections in real time for the best results.

# Installation:
First download the files from github, then place the downloaded ```spikepy.py``` into your project folder. Open the folder with VSCode, in the extension tab search "Pybricks Runner" and install if you haven't already. Then open the terminal and do ```pip install pybricksdev```. Now you can import everything in your ```main.py``` by doing ```from spikepy import *``` then just connect the hub with pybricks runner and make sure to always run the code when you have your ```main.py``` file open.

### Simplification:

1. Download ```spikepy.py``` and place it into your project.
2. Download "Pybricks Runner" extension in vscode.
3. Run ```pip install pybricksdev``` in your terminal.
4. In your ```main.py``` do ```from spikepy import *```.
5. Connect to the hub and run using the "Pybricks Runner".


# Code:

## class Robot:

This is the main robot object, used to execute all movements.

```python
    class Robot(
        hub: PrimeHub,
        left_wheel: Wheel,
        right_wheel: Wheel,
        axle_len: int,
        direction: Direction = Direction.FORWARD,
        verbose: bool = True,
        battery_low: int = 7380,
        battery_high:int = 8500
    )
```

| Name | Type | Desc |
| -- | -- | -- |
| hub | PrimeHub | The hub object. |
| left_wheel | Wheel | The left wheel of the bot. |
| right_wheel | Wheel | The right wheel of the bot. |
| axel_len | int | Distance between the center of wheels in mm. |
| **-Optional-** |
| direction | Direction | The direction the robot considers forward. |
| verbose | bool | If true the robot will send inforamtion to the pc. This is ILLEGAL in most cometitions if connected with bluetooth, so turn it off before competing, by default it is `True`. |
| battery_low | int | Level in mV at which to toggle low level battery warning. |
| battery_high | int | Level in mV at which to toggle high level battery warning. By default it is set 8500mV and the max of the battery is 8400mV. |

## Methods:

### move()

Moves the robot in a straight line for a set distance in mm with a max speed and acceleration.

```python
    def move(
        speed: int,
        dist: int,
        stop_end: bool = True,
        one_time_pid: Pid = None,
        one_time_acc: float = None,
        verbose: bool = None
    )
```

| Name | Type | Desc |
| -- | -- | -- |
| speed | int | The max speed of the movement in mm/s. |
| dist | int | The distance to travel in mm, negative means backward. |
| acc | int | The acceleration and deceleration in  mm/s². |
| **-Optional-** |
| stop_end | bool | If ```True``` the robot will slow down and stop at the end. |
| one_time_pid | Pid | It will use the given ```Pid()``` as the curent move_pid and then revert back. |
| one_time_acc | float | It will use the given acceleration as the curent move_acc and then revert back. |
| verbose | bool | Used to owerwrite verbose mode to ```False``` for a single move. |

---

### turn()

Turns the robot along an arc with a set angle in degrees (°) and radius in mm with a max speed and acceleration.

```python
    def turn(
        speed: int,
        angle: int,
        radius: int = 0,
        direction: Direction = Direction.FORWARD,
        stop_end: bool = True,
        one_time_pid: Pid = None,
        one_time_acc:int = None,
        verbose: bool = None
    )
```

| Name | Type | Desc |
| -- | -- | -- |
| speed | int | The max speed of the movement in mm/s. |
| angle | int | The angle to travel in degrees (°). |
| **-Optional-** |
| radius | int | The radius of the arc to travel on in mm. |
| direction | Direction | The direction to travel in (FORWARD/BACKWARD) |
| stop_end | bool | If ```True``` the robot will slow down and stop at the end. |
| one_time_pid | Pid | It will use the given ```Pid()``` as the curent turn_pid and then revert back. |
| one_time_acc | float | It will use the given acceleration as the curent turn_acc and then revert back. |
| verbose | bool | Used to owerwrite verbose mode to ```False``` for a single move. |

---

### aign()

Aligns the robot to the intendet heading +- deviation.

```python
    def align(
        speed_mul: float = 2,
        deviation: float = 1,
        one_time_pid: Pid = None,
        verbose: bool = None
    )
```
| Name | Type | Desc |
| -- | -- | -- |
| **-Optional-** |
| speed_mul | float | Multiplies the pid output used for speed, default is 2. |
| deviation | float | Sets the max deviation to reach before ending, default is +- 1°. |
| one_time_pid | Pid | It will use the given ```Pid()``` as the curent align_pid and then revert back. |
| verbose | bool | Used to owerwrite verbose mode to ```False``` for a single move. |

---

### reset_angle()

Resets the gyro to 0°, use when the robot is aligned.

```python
    def reset_angle()
```

---

### set_setting()

Applies all settings stored in the ```Setting()``` class.

```python
    def set_settings(setting : Setting)
```
| Name | Type | Desc |
| -- | -- | -- |
| setting | Setting | The setting object. |

---

### set_pid()

Sets any pid inside the robot for more precise movement execution.

```python
    def set_pid(
        pid_type: PidType,
        Kp: float = None,
        Ki: float = None,
        Kd: float = None
    )
```

| Name | Type | Desc |
| -- | -- | -- |
| pid_type | PidType | Type of pid to set. |
| **-Optional-** |
| Kp | float | The kp component, if ```None``` it will be unchanged. |
| Ki | float | The ki component, if ```None``` it will be unchanged. |
| Kd | float | The kd component, if ```None``` it will be unchanged. |

---

### stop()

Breaks the motors and stops the robot.

```python
    def stop()
```

---

### free()

Lets the motors spin freely and stops the robot.

```python
    def free()
```

---

### wait_for_button()

Waits for any side button to be pressed.

```python
    def wait_for_button(
        delay_after: int = 200,
        freq: int = None
    )
```

| Name | Type | Desc |
| -- | -- | -- |
| **-Optional-** |
| delay_after | int | Delay in ms that the robot will wait after the press before continuing. |
| freq | int | If set it will beep at that frequency untill pressed. |

---

## Attributes:

### hub: PrimeHub

The hub object.

---

### left_wheel: Wheel

The left wheel object.

---

### right_wheel: Wheel

The right wheel object.

---

### dec_bias: int

The distance you will start to decelerate later than normal. This is to still have some speed at the final distance. Used to prevent speed dropping to 0 before reaching the desired distance. In mm.

---

### move_bias: int

The distance the robot will stop early to account for absolute wheel slip, in mm.

---

### turn_bias: int

The angle the robot will stop early to account for absolute slip, in degrees (°)

---

### move_pid: Pid

The pid object used for ```move()```

---

### turn_pid: Pid

The pid object used for ```turn()```

---

## class Wheel:

The Wheel class is used to store all the information about a wheel and to execute moves.

```python
class Wheel(
    port: Port,
    rad: int,
    ratio: float = 1)
```

| Name | Type | Desc |
| -- | -- | -- |
| port | Port | Port the motor is connected into. |
| rad | int | Radius of the wheel in mm. |
| **-Optional-** |
| ratio | float | The ratio between the motor and the wheel. |

## class Pid:

Pid objects are passed to the robot to be used to accurately calculate the correction from gyro deviation.

```python
class Pid(
    kp: float,
    ki: float,
    kd: float)
```

---

## enum PidType:

```PidType.MOVE``` - used for keeping the robot facing forward in a straight line, when using ```move(...)```.

```PidType.TURN``` - used for keeping the robot facing along the arc, when using ```turn(...)```.

```PidType.FOLLOW``` - used for keeping the robot following the target function, when using ```follow(...)```.

---

## enum Direction:

```Direction.FORWARD``` - A positive speed value should make the motor move forward.

```Direction.BACKWARD``` - A positive speed value should make the motor move backward.

```Direction.RIGHT```

```Direction.LEFT```

```Direction.CLOCKWISE``` - A positive speed value should make the motor move clockwise.

```Direction.COUNTERCLOCKWISE``` - A positive speed value should make the motor move counterclockwise.

---

## class Setting:

This Settings class can store all configurable values for the robot, it is used to calibrate only a part of the code, by applying it with ```Robot.set_setting(...)```.

```python
    def Setting(
        move_acc: float = None,
        turn_acc: float = None,
        move_pid: Pid = None,
        turn_pid: Pid = None,
        follow_pid: Pid = None,
        align_pid: Pid = None,
        move_bias: float = None,
        turn_bias: float = None,
        min_speed: float = None
    )
```

| Name | Type | Desc |
| -- | -- | -- |
| **-Optional-** |
| move_acc | float | Acceleration used for ```move(...)```. |
| turn_acc | float | Acceleration used for ```turn(...)```. |
| move_pid | Pid | Pid used for ```move(...)```. |
| turn_pid | Pid | Pid used for ```turn(...)```. |
| follow_pid | Pid | Pid used for ```follow(...)```. |
| align_pid | Pid | Pid used for ```align(...)```. |
| move_bias | float | Bias used to stop ```move(...)``` set millimeters before the end to balance absolute overshoting. |
| turn_bias | float | Bias used to stop ```turn(...)``` set degrees before the end to balance absolute overshoting. |
| min_speed | float | The minimal speed the robot will slow down to. |