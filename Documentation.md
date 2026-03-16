# About SpikePy:
place holder

# Instalation:
place holder

# Code:

## class Robot:

This is the main robot object, used to execute all movements.

```python
class Robot(
    hub: PrimeHub,
    left_wheel: Wheel,
    right_wheel: Wheel,
    axel_len: int,
    direction: Direction = Direction.FORWARD):
```

| Name | Type | Desc |
| -- | -- | -- |
| hub | PrimeHub | The main hub of the robot. |
| left_wheel | Wheel | Left wheel object |
| right_wheel | Wheel | Right wheel object |
| axel_len | int | The distance between the wheels (center to center) in mm. |
| **-Optional-** |
| direction | Direction | Changes the whole direction of the bot (FORWARD/BACKWARD). |

## Methods:

---

### move()

Moves the robot in a straight line for a set distance in mm with a max speed and acceleration.

```python
move(
    speed: int,
    dist: int,
    acc: int = 900,
    stop_end: bool = True,
    one_time_pid: Pid = None)
```

| Name | Type | Desc |
| -- | -- | -- |
| speed | int | The max speed of the movement in mm/s. |
| dist | int | The distance to travel in mm, negative means backward. |
| acc | int | The acceleration and deceleration in  mm/s². |
| **-Optional-** |
| stop_end | bool | If ```True``` the robot will slow down and stop at the end. |
| one_time_pid | Pid | It will use the given ```Pid()``` as the curent move_pid and then revert back. |

---

### turn()

Turns the robot along an arc with a set angle in degrees (°) and radius in mm with a max speed and acceleration.

```python
turn(
    speed: int,
    angle: int,
    radius: int = 0,
    direction: Direction = Direction.FORWARD,
    acc:int = 800,
    stop_end: bool = True,
    one_time_pid: Pid = None)
```

| Name | Type | Desc |
| -- | -- | -- |
| speed | int | The max speed of the movement in mm/s. |
| angle | int | The angle to travel in degrees (°). |
| **-Optional-** |
| radius | int | The radius of the arc to travel on in mm. |
| acc | int | The acceleration and deceleration in mm/s². |
| stop_end | bool | If ```True``` the robot will slow down and stop at the end. |
| one_time_pid | Pid | It will use the given ```Pid()``` as the curent move_pid and then revert back. |

---

### reset_angle()

Resets the gyro to 0°, use when the robot is aligned.

```python
reset_angle()
```

---

### set_pid()

Sets any pid inside the robot for more precise movement execution.

```pyton
set_pid(
    pid_type: PidType,
    Kp: float = None,
    Ki: float = None,
    Kd: float = None)
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
stop()
```

---

### wait_for_button()

Waits for any side button to be pressed.

```python
wait_for_button()
```

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

The distance you will start to decelerate later then normal to still have some speed at the final distance. Used to prevent speed dropping to 0 before reaching the desired distance. In mm.

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

The Wheel class is used to store all
information about a wheel and to execute moves.

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