#!/usr/bin/env python3
""""
Contains final project code for CSSE120.
Author: Victoria Szalay
"""

import robot_controller as robo

import time
import ev3dev.ev3 as ev3
import mqtt_remote_method_calls as com

class MyDelegate(object):
    """receives function calls from PC"""
    def __init__(self):
        self.running = True
        self.n = 0
        self.time = 0

    def call_function(self, string_function_call,string_time_selected):
        print("Received: {}{} ".format(string_function_call,string_time_selected))
        if string_function_call == "seek()":
            self.n = seek()
            self.time = int(string_time_selected)
        elif string_function_call == "hide()":
            self.n = hide()
            self.time = int(string_time_selected)


def main():
    print("--------------------------------------------")
    print(" LED Button communication")
    print(" Press Back to exit when done.")
    print("--------------------------------------------")
    ev3.Sound.speak("LED Button communication").wait()

    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()



    while my_delegate.running:
        send_score(mqtt_client,str(score(my_delegate)))
        time.sleep(0.01)


def seek():
    """The robot is to find the person hiding."""
    start = time.time()
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
        elif 100 <= x <= 150:
            robot.drive_forever(drive_speed,drive_speed)
        elif 150 < x < 200:
            robot.stop_motors()
            print("Found fluffball!")
            end = time.time()
            total = end - start
            return total
        time.sleep(0.25)

    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()


def hide():
    """The robot is to randomly pick a path and follow it until time runs out to hide."""
    start = time.time()
    robot = robo.Snatch3r
    ev3.Sound.speak("I am hiding.")
    time.sleep(3)
    end = time.time()
    total = end - start
    return total


def return_to_home():
    """The robot is to return to home base once return base button is pushed on pc"""
    start = time.time()
    robot = robo.Snatch3r
    robot.seek_beacon()
    end = time.time()
    total = end - start
    return total

def score(hi):
    if hi.n > hi.time:
        return 0
    elif hi.n <= hi.time:
        score = hi.n*hi.time
        return score

def send_score(mqtt_client,score):
    mqtt_client.send_message("received_score", [score])



main()