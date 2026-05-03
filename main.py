from spikepy import *

hub = PrimeHub()

# DDM:

left_port = Port.F
right_port = Port.B
actuator_port = Port.A

wheel_rad = 24
axel_len = 95


# Home:

# left_port = Port.A
# right_port = Port.E
# actuator_port = Port.F

# wheel_rad = 29
# axel_len = 96

left_wheel = Wheel(left_port, wheel_rad)
right_wheel = Wheel(right_port, wheel_rad)
actuator = Actuator(actuator_port)

bot = Robot(hub, left_wheel, right_wheel, axel_len)


# bot.move_pid = Pid(2, 0, 1)
# bot.turn_pid = Pid(3, 0, 2)
bot.reset_angle()
actuator.set_actuator(-10, 90, 0)

bot.turn_bias = 2

bot.move(480, 400)
bot.turn(450, -15, 510)
bot.turn(450, 15, 410)
bot.move(350, 160)
bot.move(480, -30)
bot.move(480, 45)
actuator.actuate(800, 30)
bot.move(300, -20)
actuator.actuate(800, 100)
bot._default_gyro = 10
bot.move(200, -400, one_time_pid= Pid(15, 1, 9))
bot.move(480, -400)


print("Done")