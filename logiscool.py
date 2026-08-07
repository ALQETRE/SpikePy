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

bot.turn_bias = 3

bot.turn(480, 45, 20)
bot.move(480, 180)
bot.turn(480, 45, 20)

bot.move(480, 400)
bot.turn(480, 180, 160)

bot.move(480, 380)
bot.turn(480, 45)
bot.move(480, 440)
bot.turn(480, -45)
bot.move(480, 290)

bot.turn(480, -90, 80)
bot.turn(480, 90, 80, Direction.BACKWARD)
bot.move(480, 110)
bot.turn(480, -180, 160)

bot.move(480, 350)
bot.turn(480, -45)
bot.move(480, 310)
bot.turn(480, 45)
bot.move(480, 300)

# bot.turn(480, 90, 160)
# bot.move(480, 400)
# bot.turn(480, 180, 160)
# bot.move(480, 1000)
# bot.turn(480, 90, 60)
# bot.turn(480, -90, 60, Direction.BACKWARD)
# bot.move(480, 100)
# bot.turn(480, 180, 160)
# bot.move(480, 1000)
# bot.turn(480, 90, 80)

print("Done")