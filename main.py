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

bot.move(480, 200*4)
bot.move(480, -200*4)

bot.turn(480, 180, one_time_acc= 250)

bot.move(480, -200)
bot.move(480, -200)
bot.turn(480, -90, one_time_acc= 400)
bot.turn(480, 180, 200, direction= Direction.BACKWARD, one_time_acc= 300)
bot.turn(480, -90, one_time_acc= 400)


bot.turn(480, -360, one_time_acc= 250)

print("Done")