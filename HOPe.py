from spikepy import *

hub = PrimeHub()

left_port = Port.F
right_port = Port.A

left_actuator_port = Port.D
right_actuator_port = Port.B

track_port = Port.C

wheel_rad = 24
axel_len = 95

track_sens = ColorSensor(track_port)
colors = {'Lime': Color(h=89, s=64, v=93), 'Yellow': Color(h=56, s=61, v=100), 'White': Color(h=0, s=0, v=100), 'Blue': Color(h=218, s=92, v=78), 'Red': Color(h=354, s=90, v=86), 'Orange': Color(h=16, s=73, v=100), 'Green': Color(h=159, s=75, v=60), 'None': Color.NONE}
track_sens.detectable_colors(list(colors.values()))

left_wheel = Wheel(left_port, wheel_rad)
right_wheel = Wheel(right_port, wheel_rad)

actuator_left = Actuator(left_actuator_port)
actuator_right = Actuator(right_actuator_port)

bot = Robot(hub, left_wheel, right_wheel, axel_len)

def blue():
    bot.move(400, 100, one_time_acc= 400)
    bot.move(400, -100, one_time_acc= 500)

def green():
    bot.turn(400, 360)

def do_track():
    check = True
    while check:
        bot.wait_for_button(freq= None, delay_after= 50) # freq = 500

        # left_motor.run(-400)
        # right_motor.run(-400)
        # wait(100)

        bot.stop()

        check = False

        track_color = track_sens.color()

        # print(track_color)
        # print(color_sensor.hsv())
        # print()
        # return

        # await orange_track()

        if track_color == colors["Blue"]:
            blue()
        elif track_color == colors["Green"]:
            green()

        else:
            bot.hub.speaker.beep(700, 400)
            wait(100)
            bot.hub.speaker.beep(700, 400)
            check = True
    bot.free()


while True:
    do_track()