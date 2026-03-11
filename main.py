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

bot.reset_angle()
# bot.turn(300, 90, 48)
bot.move(300, 1000, stop_end= True, acc= 500)

print("Done")