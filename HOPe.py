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

bot = Robot(hub, left_wheel, right_wheel, axel_len, battery_low= 7400, battery_high= 8500, verbose= True)


def lime():
    lime_settings = Setting(
        move_acc= None,
        turn_acc= None,
        move_pid= None,
        turn_pid= None,
        align_pid= None,
        move_bias= None,
        turn_bias= None,
        min_speed= None
    )
    bot.set_settings(lime_settings)

    actuator_right.set_actuator(2.8, 90, 0)

    bot.reset_angle()

    actuator_right.actuate(500, 100, False)
    bot.move(450, 420)

    actuator_right.actuate(100, -10, False)
    bot.move(260, 120, one_time_acc= 400)

    bot.move(480, -150, one_time_acc= 1000)

    actuator_right.actuate(500, 100, False)
    bot.move(300, -400)


def template():
    _settings = Setting(
        move_acc= None,
        turn_acc= None,
        move_pid= None,
        turn_pid= None,
        follow_pid= None,
        align_pid= None,
        move_bias= None,
        turn_bias= None,
        min_speed= None
    )
    bot.set_settings(_settings)

    bot.reset_angle()
    
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

        if track_color == colors["Lime"]:
            lime()
        elif track_color == colors["Green"]:
            # green()
            pass
        else:
            bot.hub.speaker.beep(700, 400)
            wait(100)
            bot.hub.speaker.beep(700, 400)
            check = True
    bot.free()


while True:
    do_track()