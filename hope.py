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

# def green_track():

#     reset_gyro()

#     move(fast_speed, 740)
#     turn(green_turn, -50, radius=WHEEL_ROTATION)
#     turn(green_turn, 5)
#     move(fast_speed - 200, -160)
#     turn(green_turn, 90, radius=WHEEL_ROTATION)

#     move(fast_speed - 200, 60)
#     move(fast_speed, -5)
#     await actuator.actuate(1200, 0)
#     turn(fast_speed, -50, radius=-WHEEL_ROTATION)


#     await actuator.actuate(1000, 150)

#     move(fast_speed, 50)
#     turn(green_turn, -45, radius=WHEEL_ROTATION)
#     default_gyro = 88 # krystofire88
#     move(fast_speed, 500)



blue_track()

print("Done")