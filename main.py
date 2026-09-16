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

while True:
    bot.reset_angle()

    bot.turn(450, 90, 200, stop_end= False, one_time_min_speed= 300)
    bot.move(450, 200)

    wait(1000)

    print(bot._angle())

    bot.wait_for_button()

print("Done")