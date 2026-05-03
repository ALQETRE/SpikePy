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
    bot.move_pid = Pid(3, 1, 3) # <- Try more sensitive or no I component
    bot.turn_pid = Pid(3, 1, 3)

    bot.turn_bias = 2

    # bot.move(400, -40) # <- try

    bot.reset_angle()
    actuator.set_actuator(-10, 90, 0)

    bot.move(480, 400) # <- add one_time_pid
    bot.turn(450, -15, 510)
    bot.turn(450, 15, 410)
    bot.move(350, 160)
    bot.move(480, -30)
    bot.move(480, 45)
    actuator.actuate(800, 30)
    bot.move(300, -20)
    actuator.actuate(800, 100)
    bot._default_gyro = 10
    bot.move(200, -400, one_time_pid= Pid(15, 1, 9)) # <- try to remove one_time_pid
    bot.move(480, -400)


blue_track()

print("Done")