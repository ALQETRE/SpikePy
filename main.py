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

dist_sens = UltrasonicSensor(Port.D)

def until_wall(bot, target_dist):
    dist = dist_sens.distance()
    return dist - target_dist

def until_under(bot, aprox_dist):
    dist = dist_sens.distance()
    under = dist < 100 and dist > 1

    if under: 
        return 0
    else:
        return max(aprox_dist - abs(bot.dist_traveled), 10)

def until_radar(bot, aprox_angle):
    dist = dist_sens.distance()
    under = dist < 100 and dist > 1

    if under: 
        return 0
    else:
        return max(bot.get_dist_to_target_from_angle(aprox_angle - abs(bot.angle_traveled)), 10)


bot.until(200, bot.turn_loop, until_radar, bot.turn_pid, bot.turn_acc, stop_func_args= [180])

bot.wait_for_button()

bot.until(400, bot.move_loop, until_under, bot.move_pid, bot.move_acc, [200])

bot.wait_for_button()

bot.until(400, bot.move_loop, until_wall, bot.move_pid, bot.move_acc, [120])


wait(500)

print(dist_sens.distance())

print("Done")