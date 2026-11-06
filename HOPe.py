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

bot = Robot(hub, left_wheel, right_wheel, axel_len, battery_low= 7450, battery_high= 8500, verbose= True)


def lime():
    lime_settings = Setting(
        move_acc= 600,
        turn_acc= 300,
        move_pid= Pid(3, 1, 3),
        turn_pid= Pid(0.5, 0, 0.5),
        align_pid= Pid(5, 5, 1),
        move_bias= 0,
        turn_bias= 0,
        min_speed= 50
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

def blue():
    blue_settings = Setting(
        move_acc= 300,
        turn_acc= 200,
        move_pid= Pid(0.5, 0, 0.5),
        turn_pid= Pid(0.5, 0, 1.5),
        align_pid= Pid(5, 5, 1),
        move_bias= 0,
        turn_bias= 0,
        min_speed= 50
    )
    bot.set_settings(blue_settings)

    actuator_left.set_actuator(-2.8, 60, -35)
    actuator_right.set_actuator(1.67, 360, 125)
    
    bot.reset_angle()

    actuator_left.actuate(300, 100, False)
    actuator_right.actuate(300, 6, False)

    bot.move(350, 465, one_time_acc= 200)

    bot.move(350, -60)
    bot.turn(300, 90)
    bot.move(300, 192)
    bot.turn(300, -90)
    bot.move(350, 512)

    # bot.align()

    actuator_right.actuate(300, 140, True)
    
    # bot.move(350, 25)
    # wait(1000)

    bot.move(350, -95)
    bot.turn(300, -45)
    bot.move(350, -20)
    actuator_left.actuate(300, 5)
    bot.move(350, 50)
    actuator_left.actuate(300, 100)
    bot.move(350, -150)
    bot.turn(300, 45)
    bot.move(350, -700)

def orange():
    orange_settings = Setting(
        move_acc= 350,
        turn_acc= 200,
        move_pid= Pid(3, 1, 3),
        turn_pid= Pid(0.5, 0, 0.5),
        align_pid= Pid(5, 5, 1),
        move_bias= 0,
        turn_bias= 0,
        min_speed= 50
    )
    bot.set_settings(orange_settings)

    actuator_right.set_actuator(2.88, 55, 0)
    actuator_left.set_actuator(1.67, 25, 0)

    bot.reset_angle()

    bot.move(350, 85)

    bot.turn(300, -45)

    bot.move(300, 370)

    actuator_right.actuate(300, 100)

    bot.turn(300, -80, radius= bot.WHEEL_ROTATION)
    bot.move(350, 150)
    bot.turn(300, 90, radius= bot.WHEEL_ROTATION)

    bot.move(350, 200)



def template():
    _settings = Setting(
        move_acc= 350,
        turn_acc= 200,
        move_pid= Pid(3, 1, 3),
        turn_pid= Pid(0.5, 0, 0.5),
        align_pid= Pid(5, 5, 1),
        move_bias= 0,
        turn_bias= 0,
        min_speed= 50
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
        elif track_color == colors["Blue"]:
            blue()
        elif track_color == colors["Orange"]:
            orange()
        else:
            bot.hub.speaker.beep(700, 400)
            wait(100)
            bot.hub.speaker.beep(700, 400)
            check = True
    bot.free()


while True:
    do_track()