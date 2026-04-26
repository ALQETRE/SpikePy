from spikepy import *

hub = PrimeHub()

# DDM:

# left_port = Port.F
# right_port = Port.B

# wheel_rad = 29 # <- Wrong!
# axel_len = 96


# Home:

left_port = Port.A
right_port = Port.E
actuator_port = Port.F

wheel_rad = 29
axel_len = 96

left_wheel = Wheel(left_port, wheel_rad)
right_wheel = Wheel(right_port, wheel_rad)
actuator = Actuator(actuator_port)

bot = Robot(hub, left_wheel, right_wheel, axel_len)


bot.reset_angle()
# bot._default_gyro = 80

# bot.move(480, 200, stop_end= False)
# bot.turn(400, 90, 300, acc= 800)

actuator.set_actuator(1, 90, 0)
actuator.rotate(500, 210)
actuator.actuate(500, 100)
actuator.actuate(500, 0)

print("Done")