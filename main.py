from spikepy import *

hub = PrimeHub()

left_port = Port.A
right_port = Port.E
# actuator_port = Port.F

wheel_rad = 28
axel_len = 96

left_wheel = Wheel(left_port, wheel_rad)
right_wheel = Wheel(right_port, wheel_rad)
# actuator = Actuator(actuator_port)

bot = Robot(hub, left_wheel, right_wheel, axel_len)

bot._default_gyro = 20
bot.move(480, 195*3, acc= 600)

print("Done")