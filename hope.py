from spikepy import *

hub = PrimeHub()

left_port = Port.F
right_port = Port.B
actuator_port = Port.A

wheel_rad = 24
axel_len = 95

left_wheel = Wheel(left_port, wheel_rad)
right_wheel = Wheel(right_port, wheel_rad)
actuator = Actuator(actuator_port)

bot = Robot(hub, left_wheel, right_wheel, axel_len)


def blue_track():

    blue_setting = Setting(
        Pid(4, 1, 4),
        Pid(3, 1, 3),
        None,
        None,
        0,
        2,
        1
    )
    bot.set_settings(blue_setting)

    # bot.move(400, -40) # <- try

    bot.reset_angle()
    actuator.set_actuator(-10, 90, 0)

    bot.move(480, 400, one_time_pid= Pid(0, 0, 0))
    bot.turn(450, -15, 510)
    bot.turn(450, 15, 410)
    bot.move(350, 160)
    bot.move(480, -30)
    bot.move(480, 45)
    actuator.actuate(800, 30)
    bot.move(300, -20)
    actuator.actuate(800, 100)
    bot._default_gyro = 10
    bot.move(200, -400, one_time_pid= Pid(10, 1, 7))
    bot.move(480, -400)


def green_track():

    green_setting = Setting(
        Pid(4, 1, 4),
        Pid(4, 2, 3),
        None,
        None,
        0,
        3,
        1
    )
    bot.set_settings(green_setting)

    bot.reset_angle()
    actuator.set_actuator(2, 150, 110)


    bot.move(480, 750, one_time_pid= Pid(0, 0, 0))
    bot.turn(250, -47, bot.WHEEL_ROTATION)
    bot.turn(250, 11, bot.WHEEL_ROTATION)
    bot.move(300, -155)
    bot.turn(250, 85, bot.WHEEL_ROTATION)

    bot.move(300, 30)
    actuator.actuate(1000, 0)
    bot.move(400, -10)

    # bot.wait_for_button()
    print()
    print()
    print()

    bot.turn(480, 35, bot.WHEEL_ROTATION + 10, direction= Direction.BACKWARD) # Overchutes bc obstacle
    bot._default_gyro = 90


    actuator.actuate(1000, 100)


    # bot.move(480, 50)
    # bot.turn(250, 45, bot.WHEEL_ROTATION, direction= Direction.BACKWARD)
    # bot._default_gyro = 88 # krystofire88
    bot.move(480, 500, one_time_pid= Pid(6, 1, 5))

def orange_track():
    bot.move_pid = Pid(3, 0, 10)

    bot.move_bias = 0

    orange_setting = Setting(
        Pid(3, 0, 10),
        None,
        None,
        None,
        0,
        None,
        1
    )
    bot.set_settings(orange_setting)

    bot.reset_angle()

    bot.move(600, 1880)

def azure_track():

    azure_setting = Setting(
        Pid(4, 1, 4),
        Pid(3, 1, 3),
        None,
        Pid(5, 3, 8),
        0,
        1,
        1
    )
    bot.set_settings(azure_setting)

    bot.reset_angle()
    actuator.set_actuator(2, 100, 0)

    actuator.actuate(500, 100)
    bot._default_gyro = 1
    bot.move(480, 420)
    wait(300) # Probably remove
    for i in range(4):
        bot.align()
        actuator.actuate(1500, 0)
        actuator.actuate(500, 100)
    bot._default_gyro = 0


    bot.align()

    bot.turn(400, -96)

    # move(pjecet, 465)
    # turn(shtyrzhysta, -90, radius=WHEEL_ROTATION)
    bot.move(400, 345)
    bot.turn(400, 21)
    actuator.actuate(500, -20)
    bot.reset_angle()
    bot.turn(300, -140)
    bot.reset_angle()
    bot.move(500, 500)

def white_track():

    white_setting = Setting(
        Pid(4, 1, 4),
        Pid(2, 0, 5),
        None,
        Pid(5, 3, 8),
        0,
        3,
        1
    )
    bot.set_settings(white_setting)

    bot.reset_angle()
    
    bot.move(480, 650, one_time_pid= Pid(0, 0, 0))
    bot.turn(150, -80)
    bot.move(420, 440)
    bot.turn(150, 80)
    bot.align()
    bot.move(150, 270)

    bot.move(300, -210)
    bot.move(400, 95)
    bot.turn(350, 80)

    bot.move(350, 90)
    bot.turn(300, 50, acc= 600)

    bot.move(300, 200)
    bot.move(300, -100)
    bot.turn(350, -40)
    bot.turn(350, 80, 350)
    bot.move(480, 500)


def magenta_track():
    magenta_setting = Setting(
        Pid(4, 3.1, 4),
        Pid(2, 0, 5),
        None,
        Pid(5, 3, 8),
        0,
        3,
        1
    )
    bot.set_settings(magenta_setting)

    bot.reset_angle()
    actuator.set_actuator(2, 50, 50)

    bot._default_gyro = 15
    bot.move(350, 900)
    actuator.rotate(900, -360*12)
    actuator.rotate(900, 360*4)

    bot.move(400, -1000)

def yellow_track():
    yellow_setting = Setting(
        Pid(4, 1, 4),
        Pid(2, 0, 5),
        None,
        Pid(5, 3, 8),
        0,
        10,
        1
    )
    bot.set_settings(yellow_setting)

    bot.move(400, 400)
    bot.move(300, -80)
    bot.turn(400, -43, bot.WHEEL_ROTATION, Direction.BACKWARD)
    bot.move(400, 340)
    bot.turn(400, 50)




color_sensor = ColorSensor(Port.D)
CUSTOM_MAGENTA = Color(340, 100, 100)
CUSTOM_AZURE = Color(200, 100, 100)
color_sensor.detectable_colors([Color.RED, Color.BLUE, Color.YELLOW, Color.WHITE, Color.GREEN, CUSTOM_AZURE, CUSTOM_MAGENTA])

def do_track():
    check = True
    while check:
        bot.wait_for_button(freq= None) # Freq 300

        # left_motor.run(-400)
        # right_motor.run(-400)
        wait(100)

        bot.stop()

        check = False

        track_color = color_sensor.color()
        print(track_color)

        # await orange_track()

        if track_color == Color.BLUE:
            blue_track()
        elif track_color == Color.WHITE:
            white_track()
        elif track_color == Color.GREEN:
            green_track()
        elif track_color == CUSTOM_AZURE:
            azure_track()
        elif track_color == CUSTOM_MAGENTA:
            magenta_track()
        elif track_color == Color.YELLOW:
            orange_track()
        elif track_color == Color.RED:
            yellow_track()

        else:
            bot.hub.speaker.beep(700, 400)
            wait(100)
            bot.hub.speaker.beep(700, 400)
            check = True
    bot.free()


while True:
    do_track()

print("Done")
wait(10)