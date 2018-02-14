#!/usr/bin/env python3
""""
Contains final project code for CSSE120.
Author: Victoria Szalay
"""
import robot_controller as robo

import time
import ev3dev.ev3 as ev3


def main():
    seek()


def seek():
    """The robot is to find the person hiding."""
    robot = robo.Snatch3r()
    robot.pixy.mode = "SIG1"
    drive_speed = 400
    while not robot.touch_sensor.is_pressed:

        # Read the Pixy values for x and y
        # Print the values for x and y
        x = robot.pixy.value(1)
        y = robot.pixy.value(2)

        print("value1: X", x)
        print("value2: Y", y)
        if x < 100:
            robot.drive_forever(-drive_speed, drive_speed)
        elif x > 200:
            robot.drive_forever((drive_speed,-drive_speed))
            return
        elif 100 <= x <= 150:
            robot.drive_forever(drive_speed,drive_speed)
        elif 150 < x < 200:
            robot.stop_motors()
            print("Found fluffball!")
            return True
        time.sleep(0.25)

    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()

def hide():
    """The robot is to find the wisher gold and deliver it to a certain location."""
def return_to_home():
    """The robot is to return to home base once return base button is pushed on pc"""
    robot = robo.Snatch3r
    robot.seek_beacon()


main()