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

bot.move(300, 200*4)
bot.move(300, -200*4)

bot.turn(300, 180, acc= 250)

bot.move(300, -200)
bot.move(300, -200)
bot.turn(300, -90, acc= 400)
bot.turn(300, 180, 200, direction= Direction.BACKWARD, acc= 300)
bot.turn(300, -90, acc= 400)


bot.turn(300, -360, acc= 250)

print("Done")