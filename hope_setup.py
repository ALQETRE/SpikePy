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

left_wheel = Wheel(left_port, wheel_rad)
right_wheel = Wheel(right_port, wheel_rad)

actuator_left = Actuator(left_actuator_port)
actuator_right = Actuator(right_actuator_port)

bot = Robot(hub, left_wheel, right_wheel, axel_len)

colors = {
    "Blue": Color.BLUE,
    "Green": Color(120, 100, 80),
    "Lime": Color(65, 100, 100),
    "Yellow": Color(43, 100, 100),
    "Orange": Color.ORANGE,
    "White": Color.WHITE,
    "Red": Color.RED
}

real_colors = {"None": Color.NONE}


for name, color in colors.items():
    bot.hub.light.on(color)
    print()
    print(f"Now calibrating: {name}")

    real_color = None

    light_threashold = 20
    while True:
        light = track_sens.reflection()
        if light > light_threashold:
            break
        if bot.hub.buttons.pressed():
            bot.wait_for_button(delay_after= 50)
            break

    wait(500)

    while True:
        light = track_sens.reflection()
        if light > light_threashold:
            break

    wait(100)
        
    # bot.wait_for_button(delay_after= 300)

    color_done = False
    while not color_done:
        real_color = track_sens.hsv()
        print(real_color)

        bot.hub.light.off()
        wait(200)
        bot.hub.speaker.beep(400, 200)
        bot.hub.light.on(color)

        real_colors[name] = real_color
        track_sens.detectable_colors(list(real_colors.values()))

        while True:
            current_color = track_sens.color()
            if current_color != real_color:
                color_done = True
                wait(500)
                break
            else:
                if bot.hub.buttons.pressed():
                    bot.wait_for_button()
                    break

    bot.hub.speaker.beep(600, 200)

print()
print(real_colors)


print("Done")