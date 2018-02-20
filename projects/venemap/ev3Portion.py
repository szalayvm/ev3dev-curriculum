import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    btn = ev3.Button()
    btn.process()
    while True:
        if btn.left:
            print("left")
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)
        # if the right button is pressed, print "right" and turn on the right LED set to red
        if btn.right:  # an if statement is used because more than one button can be pressed at a time
            print("right")
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)
        # if the up button is pressed, print "up" and turn all LEDs off
        if btn.up:
            print("up")
            ev3.Leds.all_off()
        print(robot.color_sensor.color, robot.color_sensor.reflected_light_intensity)
        if robot.touch_sensor.is_pressed:
            ev3.Sound.speak("Done")
            break
        if btn.backspace:
            break
        time.sleep(0.01)  # Best practice to have a short delay to avoid working too hard between loop iterations.

    # Best practice to leave the LEDs on after you finish a program so you don't put away the robot while still on.
    # ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
    # ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
    robot.loop_forever()  # Calls a function that has a while True: loop within it to avoid letting the program end.


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()