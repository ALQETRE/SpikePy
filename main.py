from spikepy import *

hub = PrimeHub()

# left_port = Port.F
# right_port = Port.B

# wheel_rad = 29 # <- Wrong!
# axel_len = 96

left_port = Port.A
right_port = Port.E

wheel_rad = 29
axel_len = 96

left_wheel = Wheel(left_port, wheel_rad)
right_wheel = Wheel(right_port, wheel_rad)

bot = Robot(hub, left_wheel, right_wheel, axel_len)

bot.move_pid = Pid(11, 2, 9)
# bot.move_pid = Pid(8, 2, 9)

# bot.turn_pid = Pid(0, 0, 0)
bot.turn_pid = Pid(3, 1, 3)


bot.reset_angle()
# bot._default_gyro = 80

bot.move(480, 200, stop_end= False)
bot.turn(400, 90, 300, acc= 800)

print("Done")