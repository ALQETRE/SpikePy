from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor

from pybricks.parameters import Axis, Color, Port
from pybricks.tools import wait, StopWatch

from umath import pi, cos, degrees, radians


class BatteryException(Exception):
    pass

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

        self.kp = kp / 100
        self.ki = ki / 100
        self.kd = kd / 100

        self.max_total_error = 50

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
                Port the motor is connected into.
            rad (int):
                Radius of the wheel in mm.
            ratio (float, optional):
                The ratio between the motor and the wheel, default is 1.
        """

        self.motor = Motor(port)
        self._port = port

        self._radius = rad
        self.ratio = ratio

        self._circ = 2 * pi * rad
        self._mm_to_deg = 1 / self._circ * 360 # To translate from  mm -> deg

        self.zero_speed = 25
        self.min_speed = 60
        self.max_speed = 1050

    def _run(self, speed):
        speed *= self.ratio * self._mm_to_deg

        if abs(speed) <= self.zero_speed:
            speed = 0
        elif abs(speed) <= self.min_speed:
            speed = self.min_speed * (1 if speed > 0 else -1)
        elif abs(speed) > self.max_speed:
            # print(f"Max Speed Reached ({speed})")
            speed = self.max_speed * (1 if speed > 0 else -1)

        self.motor.run(speed)

    def _stop(self):
        self.motor.brake()

    def _get_dist(self):
        dist = self.motor.angle() / self._mm_to_deg / self.ratio
        return dist
    
    def _reset(self):
        self.motor.reset_angle(0)


class Robot:
    def __init__(self, hub: PrimeHub, left_wheel: Wheel, right_wheel: Wheel, axle_len: int, direction: Direction = Direction.FORWARD, verbose: bool = True, battery_low: int = 7300, battery_high:int = 8500):
        """
        This is the main robot object, used to execute all movements.

        Arguments:
            hub (PrimeHub):
                The hub object.
            left_wheel (Wheel):
                The left wheel of the bot.
            right_wheel (Wheel):
                The right wheel of the bot.
            axle_len (int):
                Distance between the center of wheels in mm.
            direction (Direction, optional):
                The direction the robot considers forward.
            verbose (bool, optional):
                If true the robot will send inforamtion to the pc.
                This is ILLEGAL in most cometitions if connected with bluetooth, so turn it off before competing, by default it is `True`.
            battery_low (int, optional):
                Level in mV at which to toggle low level battery warning.
            battery_high (int, optional):
                Level in mV at which to toggle high level battery warning.
                By default it is set 8500mV and the max of the battery is 8400mV.
        """

        self.hub = hub
        self.verbose = verbose

        if verbose:
            print(f"VERBOSE mode is turned on, this is illegal in most competitons!\n")

        self.battery_low = battery_low
        self.battery_high = battery_high # Max of the battery is 8.4V

        self.battery_check()

        self.left_wheel = left_wheel
        self.right_wheel = right_wheel

        self.left_wheel.ratio *= -1 * direction # Swap direction for one wheel to drive forwards
        self.right_wheel.ratio *= direction

        self._dir = direction

        self._axle_len = axle_len
        self.WHEEL_ROTATION = axle_len / 2

        self._default_gyro = 0

        self._left_speed = 0
        self._right_speed = 0

        self.dec_bias = 1 # [mm]
        self.move_bias = 0
        self.turn_bias = 0

        # self.angular_slip_threshold = 5
        # self.linear_slip_threshold = 100
        # self.slip_acc = 0.2

        # self._slip = 1

        self.move_pid = Pid(3, 1, 3)
        self.turn_pid = Pid(3, 1, 3)

    def battery_check(self):
        battery_voltage = self.hub.battery.voltage()
        if battery_voltage > self.battery_high:
            if self.verbose:
                raise BatteryException(f"HIGH battery! ({battery_voltage}mV)")
            self.hub.light.blink(Color.VIOLET, [400, 200])

        if battery_voltage < self.battery_low:
            if self.verbose:
                raise BatteryException(f"LOW battery! ({battery_voltage}mV)")
            self.hub.light.blink(Color.RED, [400, 200])

    def stop(self):
        """
        Breaks the motors and stops the robot.
        """

        self.left_wheel._stop()
        self.right_wheel._stop()

        self._left_speed = 0
        self._right_speed = 0
        wait(200)

    def _angle(self):
        angle = self.hub.imu.heading()
        angle -= self._default_gyro
        return angle
    
    def _angular_vel(self):
        angular_vel = self.hub.imu.angular_velocity(Axis.Z)
        return angular_vel

    def _linear_acc(self):
        linear_acc = self.hub.imu.acceleration(Axis.Y) * self._dir
        return linear_acc

    def reset_angle(self):
        """
        Resets the gyro to 0°, use when the robot is aligned.
        """
        wait(800)
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
        return max(abs(left), abs(right)) # TODO: Try avg
    
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
        angular_vel_calc = degrees((left - right) / self._axle_len)
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



    def move(self, speed: int, dist: int, acc: int = 900, stop_end: bool = True, one_time_pid: Pid = None):
        """
        Moves the robot in a straight line for a set distance in mm with a max speed and acceleration.

        Arguments:
            speed (int):
                The max speed of the movement in mm/s.
            dist (int):
                The distance to travel in mm, negative means backward.
            acc (int, optional):
                The acceleration and deceleration in  mm/s².
            stop_end (bool, optional):
                If ```True``` the robot will slow down and stop at the end.
            one_time_pid (Pid, optional):
                It will use the given ```Pid()``` as the curent move_pid and then revert back.
        """
        
        old_pid = self.move_pid
        if not one_time_pid is None:
            self.move_pid = one_time_pid

        true_dist = abs(dist) - self.move_bias

        self.move_pid._reset(-self._angle())

        speed *= 1 if dist > 0 else -1

        dist_traveled = 0
        self._reset_slip()
        self._reset_dist()

        i = 1
        stopwatch = StopWatch()

        while abs(dist_traveled) < true_dist:

            dt = stopwatch.time() / 1000 / i
            i += 1

            current_acc = self._acceleration(speed, speed, acc, dt)

            angle = self._angle()
            correction = self.move_pid._calc(-angle, dt) * self._axle_len / 2

            # print(f"Angle: {angle}")
            # print(f"Correction: {correction}")
            # print(f"Speed scale: {self._speed_scale(-angle)}")

            speed_scale = self._speed_scale(-angle)

            left_speed = (self._left_speed * speed_scale) + correction
            right_speed = (self._right_speed * speed_scale) - correction

            # left_speed, right_speed = self._slip_correction(left_speed, right_speed, current_acc, dt)

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

    def turn(self, speed: int, angle: int, radius: int = 0, direction: Direction = Direction.FORWARD, acc: int = 800, stop_end: bool = True, one_time_pid: Pid = None):
        """
        Turns the robot along an arc with a set angle in degrees (°) and radius in mm with a max speed and acceleration.

        Arguments:
            speed (int):
                The max speed of the movement in mm/s.
            angle (int):
                The angle to travel in degrees (°).
            radius (int, optional):
                The radius of the arc to travel on in mm.
            direction (Direction, optional):
                The direction to travel in (FORWARD/BACKWARD)
            acc (int, optional):
                The acceleration and deceleration in mm/s².
            stop_end (bool, optional):
                If ```True``` the robot will slow down and stop at the end.
            one_time_pid (Pid, optional):
                It will use the given ```Pid()``` as the curent turn_pid and then revert back.
        """
        
        old_pid = self.turn_pid
        if not one_time_pid is None:
            self.turn_pid = one_time_pid

        true_angle = abs(angle) - self.turn_bias

        left_speed = 0
        right_speed = 0

        small_rad = radius - (self._axle_len / 2)
        big_rad = radius + (self._axle_len / 2)

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

        i = 1
        stopwatch = StopWatch()

        while abs(angle_traveled) < true_angle:

            dt = stopwatch.time() / 1000 / i
            i += 1

            current_acc = self._acceleration(org_left_speed, org_right_speed, acc, dt)

            angle_traveled = self._angle()

            if angle > 0:
                angle_calculated = abs(self.left_wheel._get_dist()/big_total_dist) * angle
            else:
                angle_calculated = abs(self.right_wheel._get_dist()/big_total_dist) * angle

            error = angle_calculated - angle_traveled
            error *= direction
            correction = self.turn_pid._calc(error, dt) * self._axle_len / 2

            speed_scale = self._speed_scale(error)

            left_speed = (self._left_speed * speed_scale) + correction
            right_speed = (self._right_speed * speed_scale) - correction

            # left_speed, right_speed = self._slip_correction(left_speed, right_speed, current_acc, dt)

            self.left_wheel._run(left_speed)
            self.right_wheel._run(right_speed)

            angle_traveled = self._angle()

            if stop_end:
                t_to_stop = self._calc_t_from_acc(-self._left_speed, -self._right_speed, acc)
                dist_to_stop = (abs(self._acc_combine(self._left_speed, self._right_speed)) * t_to_stop) / 2 - self.dec_bias

                if dist_to_stop > big_total_dist - abs(self.left_wheel._get_dist()):
                    org_left_speed = 0
                    org_right_speed = 0


        if stop_end:
            self.stop()
        
        self.turn_pid = old_pid

        self._default_gyro += angle * direction


class Actuator:
    def __init__(self, port: Port, ratio: float = 1, range: float = 0, current_angle: float = 0):
        """
        Actuators are used for controling other than movement motors.
        They allow you to move in a given range or indefinetly at a set speed.

        Arguments:
            port (Port):
                Port the motor is connected into.
            ratio (float, optional):
                The ratio between the motor and the moving part, default is 1.
            range (float, optional):
                The range in °, in which the moving part will operate in.
            current_angle (float, optional).
                The current angle of the moving part, at the time of initilazation,
                relative to the 0% value, default is 0°.
        """
        self.motor = Motor(port)
        self._port = port

        self._ratio = ratio
        self._range = range
        self.current_angle = current_angle

        self._total_range = ((self._range // 360) + 1) * 360
        self._opp_center = ((range / 2) + 180) % self._total_range

        self.zero_speed = 25
        self.min_speed = 60
        self.max_speed = 1050

    def actuate(self, speed: int, travel: float, wait: bool = True):
        """
        Moves the connected moving part in a range to an %.
        100% means it will be at the end of the range and 0% means it will be at 0°.

        Arguments:
            speed (int):
                The max speed of the movement in °/s.
            travel (float):
                The absolute % to travel to.
            wait (bool, optional):
                If `True` the code waits for the movement to finish, default is `True`.
        """

        desired_angle = (self._range * travel) / 100
        angle_diff = desired_angle - self.current_angle
        self.current_angle = desired_angle

        speed *= abs(self._ratio)
        if abs(speed) <= self.zero_speed:
            speed = 0
        elif abs(speed) <= self.min_speed:
            speed = self.min_speed * (1 if speed > 0 else -1)
        elif abs(speed) > self.max_speed:
            # print(f"Max Speed Reached ({speed})")
            speed = self.max_speed * (1 if speed > 0 else -1)

        self.motor.run_angle(speed, angle_diff*self._ratio, wait= wait)

    def rotate(self, speed: int, angle: float):
        """
        Rotates the actuator at a set speed for an angle.

        Arguments:
            speed (int):
                The max speed of the movement in °/s.
            angle (float):
                Angle by which to rotate. Can be negative.
        """


        speed *= abs(self._ratio)

        if abs(speed) <= self.zero_speed:
            speed = 0
        elif abs(speed) <= self.min_speed:
            speed = self.min_speed * (1 if speed > 0 else -1)
        elif abs(speed) > self.max_speed:
            # print(f"Max Speed Reached ({speed})")
            speed = self.max_speed * (1 if speed > 0 else -1)

        self.motor.run_angle(speed, angle*self._ratio)

        angle_change = angle * (1 if speed > 0 else -1)
        angle_change %= self._total_range
        if angle_change > self._opp_center:
            angle_change -= self._total_range
        self.current_angle += angle_change

    def set_actuator(self, ratio: float = None, range: float = None, current_angle: float = None):
        """
        Sets the actuator parameters. If set to `None` it will remain unchanged.

        Arguments:
            ratio (float, optional):
                The ratio between the motor and the moving part, default is 1.
            range (float, optional):
                The range in °, in which the moving part will operate in.
            current_angle (float, optional).
                The current angle of the moving part, at the time of initilazation,
                relative to the 0% value, default is 0°.
        """

        if not ratio is None:
            self._ratio = ratio
        if not range is None:
            self._range = range
        if not current_angle is None:
            self.current_angle = current_angle

        self._total_range = ((self._range // 360) + 1) * 360
        self._opp_center = ((range / 2) + 180) % self._total_range
