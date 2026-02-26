from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor

from pybricks.parameters import Axis, Color, Button, Port

from enum import Enum


hub = PrimeHub()

class Direction(Enum):
    FORWARD = 1,
    BACKWARD = -1,
    RIGHT = 1,
    LEFT = -1


class Pid:
    def __init__(self, kp, ki, kd):
        """
        PID controler

        Arguments:
            Kp (float):
                The **proportional** term.
            Ki (float):
                The **integral** term.
            Kd (float):
                The **derivative** term.
        """

        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.last_error = 0
        self.total_error = 0

    def calc(self, error, dt):
        output = 0
        output += self.kp * error
        output += self.ki * self.total_error
        output += self.kd * (error - self.last_error) / dt

        self.last_error = error
        self.total_error += error * dt

        return output
    
    def reset(self):
        self.last_error = 0
        self.total_error = 0


class Wheel:
    def __init__(self, port: Port, rad: int, ratio: float = 1):
        """
        The Wheel class is used to store all
        information about a wheel and to execute moves.

        Arguments:
            port (Port):
                The port of the motor connected to the wheel.
            rad (int):
                Radius of the wheel in mm.
            ratio (float, optional):
                The ratio, if the is a gear reduction between the wheel and the motor, default is 1.
        """

        self.motor = Motor(port)
        self.port = port

        self.radius = rad
        self.ratio = ratio


class Robot:
    def __init__(self, hub: PrimeHub, left_wheel: Wheel, right_wheel: Wheel, axel_len: int, direction: Direction = Direction.FORWARD):
        """
        This is the ROBOT base, used to execute all movements and functions.

        Arguments:
            hub (PrimeHub):
                The hub object.
            left_wheel (Wheel):
                The left wheel of the bot.
            right_wheel (Wheel):
                The right wheel of the bot.
            axel_len (int):
                Distance between the center of wheels in mm.
            direction (Direction, optional):
                The direction the robot considers forward.
        """

        self.hub = hub

        self.left_wheel = left_wheel
        self.right_wheel = right_wheel

        self.left_wheel.ratio * -1 * direction # Swap direction for one wheel to drive forwards
        self.right_wheel.ratio * direction

        self.axel_len = axel_len