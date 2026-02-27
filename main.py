from spikepy import *

hub = PrimeHub()

left_port = Port.A
right_port = Port.B

wheel_rad = 29
axel_len = 135

left_wheel = Wheel(left_port, wheel_rad)
right_wheel = Wheel(right_port, wheel_rad)

bot = Robot(hub, left_wheel, right_wheel, axel_len)

bot.move(300, 200)