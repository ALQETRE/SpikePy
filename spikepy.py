from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor

from pybricks.parameters import Axis, Color, Button, Port
from pybricks.tools import wait, StopWatch

from umath import pi, cos, degrees, radians


class Direction:
    FORWARD = 1
    """A positive speed value should make the motor move forward."""

    BACKWARD = -1
    """A positive speed value should make the motor move backward."""

    RIGHT = 1
    LEFT = -1

    CLOCKWISE = 0
    """A positive speed value should make the motor move clockwise."""

    COUNTERCLOCKWISE = 1
    """A positive speed value should make the motor move counterclockwise."""


class PidType:
    MOVE = 0
    """Move PID - used for keeping the robot facing forward in a straight line, when using ```move(...)```."""

    TURN = 1
    """Turn PID - used for keeping the robot facing along the arc, when using ```turn(...)```."""

    FOLLOW = 2
    """Follow PID - used for keeping the robot following the target function, when using ```follow(...)```."""


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

        self.max_total_error = 100

        self._last_error = 0
        self._total_error = 0

    def _calc(self, error: float, dt: float) -> float:
        if dt == 0:
            return 0
                
        output = 0
        output += self.kp * error
        output += self.ki * self._total_error
        output += self.kd * (error - self._last_error) / dt

        self._last_error = error
        self._total_error += error * dt

        if abs(self._total_error) > self.max_total_error:
            self._total_error = self.max_total_error * (1 if self._total_error > 0 else -1)

        return output
    
    def _reset(self, error= 0):
        self._last_error = error
        self._total_error = 0

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

        self.circ = 2 * pi * rad
        self.mm_to_deg = 1 / self.circ * 360 # To translate from  mm -> deg

        self.zero_speed = 25
        self.min_speed = 60

    def _run(self, speed):
        speed *= self.ratio * self.mm_to_deg

        if abs(speed) <= self.zero_speed:
            speed = 0
        elif abs(speed) <= self.min_speed:
            speed = self.min_speed

        self.motor.run(speed)

    def _stop(self):
        self.motor.brake()

    def _get_dist(self):
        dist = self.motor.angle() / self.mm_to_deg / self.ratio
        return dist
    
    def _reset(self):
        self.motor.reset_angle(0)


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

        self.left_wheel.ratio *= -1 * direction # Swap direction for one wheel to drive forwards
        self.right_wheel.ratio *= direction

        self.dir = direction

        self._axel_len = axel_len

        self._default_gyro = 0

        self._left_speed = 0
        self._right_speed = 0

        self.dec_bias = 10 # [mm]
        self.move_bias = 0
        self.turn_bias = 0

        self.angular_slip_threshold = 5
        self.linear_slip_threshold = 5
        self.slip_acc = 0.2

        self._slip = 1

        self.move_pid = Pid(0.1, 0, 0.1)
        self.turn_pid = Pid(0.1, 0, 0.1)

    def stop(self):
        """
        Breaks the motors and stops the robot.
        """

        self.left_wheel._stop()
        self.right_wheel._stop()
        wait(200)

    def _angle(self):
        angle = self.hub.imu.heading()
        angle -= self._default_gyro
        return angle
    
    def _angular_vel(self):
        angular_vel = self.hub.imu.angular_velocity(Axis.Z)
        return angular_vel

    def _linear_acc(self):
        linear_acc = -self.hub.imu.acceleration(Axis.Y) * self.dir
        return linear_acc

    def reset_angle(self):
        """
        Resets the gyro to 0°
        """
        
        self.hub.imu.reset_heading(0)
        self._default_gyro = 0

    def wait_for_button(self):
        """
        Waits for any side button to be pressed.
        """

        while not self.hub.buttons.pressed():
            wait(50)
        wait(300)

    def set_pid(self, pid_type: PidType, Kp: float = None, Ki: float = None, Kd: float = None):
        """
        Sets any pid inside the robot for more precise movement execution.

        Arguments:
            pid_type (PidType):
                What pid to edit.
            Kp (float, optional):
                The new proportional term, if ```None``` then will be left unchanged.
            Ki (float, optional):
                The new integral term, if ```None``` then will be left unchanged.
            Kd (float, optional):
                The new derivative term, if ```None``` then will be left unchanged.
        """


        if pid_type == PidType.MOVE:
            if not Kp is None:
                self.move_pid.kp = Kp
            if not Ki is None:
                self.move_pid.ki = Ki
            if not Kd is None:
                self.move_pid.kd = Kd
        elif pid_type == PidType.TURN:
            pass
        elif pid_type == PidType.FOLLOW:
            pass

        # TODO: Add support for more types of pids

    def _get_dist(self):
        left_dist = self.left_wheel._get_dist()
        right_dist = self.right_wheel._get_dist()

        return (left_dist + right_dist) / 2
    
    def _reset_dist(self):
        self.left_wheel._reset()
        self.right_wheel._reset()

    def _acc_combine(self, left: float, right: float) -> float:
        return max(left, right) # TODO: Try avg
    
    def _calc_t_from_acc(self, left_diff: int, right_diff: int, acc: int):
        t_left = abs(left_diff) / acc
        t_right = abs(right_diff) / acc

        t = self._acc_combine(t_left, t_right)
        
        return t

    def _acceleration(self, left_speed: int, right_speed: int, acc: int, dt: float):
        left_diff = left_speed - self._left_speed
        right_diff = right_speed - self._right_speed

        t = self._calc_t_from_acc(left_diff, right_diff, acc)
        if t == 0:
            self._left_speed = left_speed
            self._right_speed = right_speed
            return 0

        left_acc = left_diff / t
        right_acc = right_diff / t


        self._left_speed += left_acc * dt
        self._right_speed += right_acc * dt

        accelerating = True

        if left_diff > 0 and self._left_speed > left_speed:
            self._left_speed = left_speed
            accelerating = False
        elif left_diff < 0 and self._left_speed < left_speed:
            self._left_speed = left_speed
            accelerating = False

        if right_diff > 0 and self._right_speed > right_speed:
            self._right_speed = right_speed
            accelerating = False
        elif right_diff < 0 and self._right_speed < right_speed:
            self._right_speed = right_speed
            accelerating = False

        return (acc if accelerating else 0) * (1 if (left_diff + right_diff) > 0 else -1)

    def _speed_scale(self, error: float) -> float:
        clamped_angle = radians(min(abs(error), 90))
        scale = cos(clamped_angle)
        return scale
    
    def _slip_correction(self, left: int, right: int, acc: int, dt: float) -> tuple:
        angular_vel_calc = degrees((left - right) / self._axel_len)
        angular_vel_measured = self._angular_vel()
        angular_vel_diff = abs(angular_vel_calc - angular_vel_measured)

        acc_measured = self._linear_acc()
        linear_acc_diff = abs(acc - acc_measured)

        if angular_vel_diff > self.angular_slip_threshold:
            self._slip -= self.slip_acc * dt
            if self._slip < 0:
                self._slip = 0
            print("SLIP A")
        elif linear_acc_diff > self.linear_slip_threshold:
            self._slip -= self.slip_acc * dt
            if self._slip < 0:
                self._slip = 0
            print("SLIP L")
        else:
            self._slip += self.slip_acc * dt
            if self._slip > 1:
                self._slip = 1
        
        return left * self._slip, right * self._slip

    def _reset_slip(self):
        self._slip = 1



    def move(self, speed: int, dist: int, acc: int = 300, stop_end: bool = True, one_time_pid: Pid = None):
        """
        Moves the robot in a straight line for a set distance in mm with a predefined speed and acceleration.

        Arguments:
            speed (int):
                Max speed of the robot during the motion in mm/s.
            dist (int):
                The distance to travel in mm.
            one_time_pid (Pid, optional):
                If a pid object is given it will be used as the PidType.MOVE for this single motion.
            acc (int, optional):
                The acceleration and deceleration in mm/s^2.
            stop_end (bool, optional):
                If true at the end of the movemnt it will slow down and stop.
        """
        
        old_pid = self.move_pid
        if not one_time_pid is None:
            self.move_pid = one_time_pid

        true_dist = abs(dist) - self.move_bias

        self.move_pid._reset(-self._angle())

        dist_traveled = 0
        self._reset_slip()
        self._reset_dist()

        stopwatch = StopWatch()

        while abs(dist_traveled) < true_dist:

            dt = stopwatch.time() / 1000
            stopwatch.reset()

            current_acc = self._acceleration(speed, speed, acc, dt)

            angle = self._angle()
            correction = self.move_pid._calc(-angle, dt) * self._axel_len / 2

            # print(f"Angle: {angle}")
            # print(f"Correction: {correction}")
            # print(f"Speed scale: {self._speed_scale(-angle)}")

            left_speed = (self._left_speed * self._speed_scale(-angle)) + correction
            right_speed = (self._right_speed * self._speed_scale(-angle)) - correction

            left_speed, right_speed = self._slip_correction(left_speed, right_speed, current_acc, dt)

            self.left_wheel._run(left_speed)
            self.right_wheel._run(right_speed)

            dist_traveled = self._get_dist()

            if stop_end:
                t_to_stop = self._calc_t_from_acc(-self._left_speed, -self._right_speed, acc)
                dist_to_stop = (abs(self._acc_combine(self._left_speed, self._right_speed)) * t_to_stop) / 2 - self.dec_bias

                if dist_to_stop > abs(dist - dist_traveled):
                    speed = 0

        if stop_end:
            self.stop()
        
        self.move_pid = old_pid

    def turn(self, speed: int, angle: int, radius: int = 0, direction: Direction = Direction.RIGHT, acc:int = 300, stop_end: bool = True, one_time_pid: Pid = None):
        """
        Moves the robot in a straight line for a set distance in mm with a predefined speed and acceleration.

        Arguments:
            speed (int):
                Max speed of the robot during the motion in mm/s.
            dist (int):
                The distance to travel in mm.
            one_time_pid (Pid, optional):
                If a pid object is given it will be used as the PidType.MOVE for this single motion.
            acc (int, optional):
                The acceleration and deceleration in mm/s^2.
            stop_end (bool, optional):
                If true at the end of the movemnt it will slow down and stop.
        """
        
        old_pid = self.turn_pid
        if not one_time_pid is None:
            self.turn_pid = one_time_pid

        true_angle = abs(angle) - self.turn_bias

        left_speed = 0
        right_speed = 0

        small_rad = radius - (self._axel_len / 2)
        big_rad = radius + (self._axel_len / 2)

        if radius != 0:
            if angle > 0:
                org_left_speed = speed * direction
                org_right_speed = speed * (small_rad / big_rad) * direction
            else:
                org_left_speed = speed * (small_rad / big_rad) * direction
                org_right_speed = speed * direction
        else:
            if angle > 0:
                org_left_speed = speed
                org_right_speed = -speed
            else:
                org_left_speed = -speed
                org_right_speed = speed

        big_total_dist = abs(big_rad * pi/180 * angle)
            
        self.turn_pid._reset(-self._angle())

        angle_traveled = 0
        self._reset_slip()
        self._reset_dist()

        stopwatch = StopWatch()

        while abs(angle_traveled) < true_angle:

            dt = stopwatch.time() / 1000
            stopwatch.reset()

            current_acc = self._acceleration(org_left_speed, org_right_speed, acc, dt)

            angle_traveled = self._angle()

            if angle > 0:
                angle_calculated = abs(self.left_wheel._get_dist()/big_total_dist) * angle
            else:
                angle_calculated = abs(self.right_wheel._get_dist()/big_total_dist) * angle

            error = angle_calculated - angle_traveled
            correction = self.turn_pid._calc(error, dt) * self._axel_len / 2

            left_speed = (self._left_speed * self._speed_scale(error)) + correction
            right_speed = (self._right_speed * self._speed_scale(error)) - correction

            left_speed, right_speed = self._slip_correction(left_speed, right_speed, current_acc, dt)

            self.left_wheel._run(left_speed)
            self.right_wheel._run(right_speed)

            angle_traveled = self._angle()

            if stop_end:
                t_to_stop = self._calc_t_from_acc(-self._left_speed, -self._right_speed, acc)
                dist_to_stop = (abs(self._acc_combine(self._left_speed, self._right_speed)) * t_to_stop) / 2 - self.dec_bias
                if angle > 0 and dist_to_stop > big_total_dist - abs(self.left_wheel._get_dist()):
                    speed = 0
                elif angle < 0 and dist_to_stop > big_total_dist - abs(self.right_wheel._get_dist()):
                    speed = 0


        if stop_end:
            self.stop()
        
        self.turn_pid = old_pid

        self._default_gyro += angle