from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor

from pybricks.parameters import Axis, Color, Button, Port
from pybricks.tools import wait, StopWatch


PI = 3.14159

class Direction:
    FORWARD = 1,
    """A positive speed value should make the motor move forward."""

    BACKWARD = -1,
    """A positive speed value should make the motor move backward."""

    RIGHT = 1,
    LEFT = -1

    CLOCKWISE = 0
    """A positive speed value should make the motor move clockwise."""

    COUNTERCLOCKWISE = 1
    """A positive speed value should make the motor move counterclockwise."""


class Pid:
    def __init__(self, kp: float, ki: float, kd: float):
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

    def calc(self, error: float, dt: float) -> float:
        if dt == 0:
            return 0
        
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

        self.circ = 2 * PI * rad
        self.mm_to_deg = 1 / self.circ * 360 # To translate from  mm -> deg

        self.zero_speed = 25
        self.min_speed = 70

    def _run(self, speed):
        speed *= self.ratio * self.mm_to_deg
        print(f"ratio: {self.ratio}")

        if abs(speed) <= self.zero_speed:
            speed = 0
        elif abs(speed) <= self.min_speed:
            speed = self.min_speed

        Motor.run(self.motor, speed)

    def _stop(self):
        Motor.brake(self.motor)

    def _get_dist(self):
        angle = Motor.angle(self.motor) / self.mm_to_deg / self.ratio
        return angle
    
    def _reset(self):
        Motor.reset_angle(self.motor, 0)


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

        self._axel_len = axel_len

        self._default_gyro = 0

        self._left_speed = 0
        self._right_speed = 0

        self.move_pid = Pid(0, 0, 0)

    def stop(self):
        self.left_wheel._stop
        self.right_wheel._stop

    def angle(self):
        angle = self.hub.imu.heading()
        angle -= self._default_gyro
        return angle
    
    def _reset_angle(self):
        self.hub.imu._reset_heading(0)

    def wait_for_button(self):
        while not self.hub.buttons.pressed():
            wait(50)
        wait(300)

    def _set_pid(self, Kp: float = None, Ki: float = None, Kd: float = None):
        if not Kp is None:
            self.move_pid.kp = Kp
        if not Ki is None:
            self.move_pid.ki = Ki
        if not Kd is None:
            self.move_pid.kd = Kd

        # TODO: Add support for more types of pids

    def _get_dist(self):
        left_dist = self.left_wheel._get_dist()
        right_dist = self.right_wheel._get_dist()

        return (left_dist + right_dist) / 2
    
    def _reset_dist(self):
        self.left_wheel._reset()
        self.right_wheel._reset()
    
    def _calc_t_from_acc(self, left_speed: int, right_speed: int, acc: int):
        left_diff = left_speed - self._left_speed
        right_diff = right_speed - self._right_speed

        t_left = abs(left_diff) / acc
        t_right = abs(right_diff) / acc

        t = max(t_left, t_right) # TODO: Try avg
        
        return t

    def _acceleration(self, left_speed: int, right_speed: int, acc: int, dt: float):
        left_diff = left_speed - self._left_speed
        right_diff = right_speed - self._right_speed

        t = self._calc_t_from_acc(left_speed, right_speed, acc)

        if t == 0:
            self._left_speed = left_speed
            self._right_speed = right_speed
            return

        left_acc = left_diff / t
        right_acc = left_diff / t

        print(f"Left acc: {left_acc}")

        self._left_speed += left_acc * dt
        self._right_speed += right_acc * dt

        if left_diff > 0 and self._left_speed > left_speed:
            self._left_speed = left_speed
        elif left_diff < 0 and self._left_speed < left_speed:
            self._left_speed = left_speed

        if right_diff > 0 and self._right_speed > right_speed:
            self._right_speed = right_speed
        elif right_diff < 0 and self._right_speed < right_speed:
            self._right_speed = right_speed


    def move(self, speed: int, dist: int, one_time_pid: Pid = None, acc= 300, stop_end= True):
        
        # TODO: Revert the old pid

        old_pid = self.move_pid
        if not one_time_pid is None:
            self.move_pid = one_time_pid

        self.move_pid.reset()

        total_dist = 0
        self._reset_dist()

        stopwatch = StopWatch()

        while abs(total_dist) < abs(dist):

            dt = stopwatch.time() / 1000
            stopwatch.reset()

            print(f"dt: {dt}")

            self._acceleration(speed, speed, acc, dt)

            angle = self.angle()
            correction = self.move_pid.calc(-angle, dt) / 2

            left_speed = self._left_speed - correction
            right_speed = self._right_speed + correction

            self.left_wheel._run(left_speed)
            self.right_wheel._run(right_speed)

            total_dist = self._get_dist()

            if stop_end:
                if speed != 0:
                    t_to_stop = self._calc_t_from_acc(0, 0, acc)
                    dist_to_stop = (abs(speed) * t_to_stop) / 2 - 10 # TODO: Dec bias (-10)
                if dist_to_stop > abs(dist - total_dist):
                    speed = 0
            print(f"Speed: {speed}")

        if stop_end:
            self.stop()
        
        self.move_pid = old_pid

