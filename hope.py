from spikepy import *

hub = PrimeHub()

left_port = Port.F
right_port = Port.B
actuator_port = Port.A

wheel_rad = 24
axel_len = 95

left_wheel = Wheel(left_port, wheel_rad)
right_wheel = Wheel(right_port, wheel_rad)
actuator = Actuator(actuator_port)

bot = Robot(hub, left_wheel, right_wheel, axel_len)


def blue_track():
    bot.move_pid = Pid(4, 1, 4) # <- Try more sensitive or no I component
    bot.turn_pid = Pid(3, 1, 3)

    bot.move_bias = 0
    bot.turn_bias = 2

    # bot.move(400, -40) # <- try

    bot.reset_angle()
    actuator.set_actuator(-10, 90, 0)

    bot.move(480, 400, one_time_pid= Pid(0, 0, 0)) # <- add one_time_pid
    bot.turn(450, -15, 510)
    bot.turn(450, 15, 410)
    bot.move(350, 160)
    bot.move(480, -30)
    bot.move(480, 45)
    actuator.actuate(800, 30)
    bot.move(300, -20)
    actuator.actuate(800, 100)
    bot._default_gyro = 10
    bot.move(200, -400, one_time_pid= Pid(10, 1, 7)) # <- try to remove one_time_pid
    bot.move(480, -400)


def green_track():

    bot.move_pid = Pid(4, 1, 4)
    bot.turn_pid = Pid(3, 1, 3)

    bot.move_bias = 0
    bot.turn_bias = 3

    bot.reset_angle()
    actuator.set_actuator(2, 150, 110)


    bot.move(480, 720, one_time_pid= Pid(0, 0, 0))
    bot.turn(250, -45, bot.WHEEL_ROTATION)
    # bot.turn(250, 5)
    bot.move(300, -170)
    bot.turn(250, 90, bot.WHEEL_ROTATION)

    bot.move(300, 50)
    bot.move(480, -10)
    actuator.actuate(1000, 0)
    print(bot._default_gyro)

    bot.turn(480, -45, bot.WHEEL_ROTATION, direction= Direction.BACKWARD)


    actuator.actuate(1000, 100)

    print(bot._default_gyro)

    # bot.move(480, 50)
    # bot.turn(250, -45, bot.WHEEL_ROTATION, direction= Direction.BACKWARD)
    # bot._default_gyro = 88 # krystofire88
    bot.move(480, 500)



green_track()

print("Done")