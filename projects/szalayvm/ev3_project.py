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
        self.m = 0
        self.time = 0

    def call_function(self, string_function_call,string_time_selected):
        print("Received: {}{} ".format(string_function_call,string_time_selected))
        if string_function_call == "seek()":
            self.n = seek(int(string_time_selected))
            self.time = int(string_time_selected)
        elif string_function_call == "hide()":
            self.m = hide(int(string_time_selected))
            self.time = int(string_time_selected)


def main():
    print("--------------------------------------------")
    print(" Hide and Go Seek")
    print(" Press Back to exit when done.")
    print("--------------------------------------------")
    ev3.Sound.speak("LED Button communication").wait()

    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()



    while my_delegate.running:
        send_score(mqtt_client,str(score(my_delegate)),str(score2(my_delegate)))
        time.sleep(0.01)


def seek(time_alloted):
    """The robot is to find the person hiding."""
    start = time.time()
    robot = robo.Snatch3r()
    robot.pixy.mode = "SIG1"
    drive_speed = 400
    total = 0
    while total < time_alloted:
        robot.seek_beacon()
        end = time.time()
        total = end - start
        return total


    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()


def hide(time_alloted):
    """The robot is to randomly pick a path and follow it until time runs out to hide."""
    start = time.time()
    ev3.Sound.speak("I am hiding.")
    robot = robo.Snatch3r()
    drive_speed = 200
    total = 0

    while total < time_alloted:
        print("Pink_distance", find_pink_distance())
        print("Green_distance", find_green_distance())
        if find_pink_distance() > 200:
            robot.turn_degrees(180,drive_speed)
            robot.drive_forever(drive_speed,drive_speed)
        if find_green_distance() < 70:
            robot.drive_forever(-drive_speed, drive_speed)
        elif find_green_distance() > 200:
            robot.drive_forever(drive_speed, -drive_speed)
        elif 70 <= find_green_distance() <= 165:
            robot.drive_forever(drive_speed, drive_speed)
        elif 165 < find_green_distance() < 200:
            robot.stop_motors()
            ev3.Sound.speak("Hidden")
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
        score = hi.time/(hi.n+1)
        return score

def score2(hi):
    if hi.m > hi.time:
        return 0
    elif hi.m <= hi.time:
        score = hi.time/(hi.m+1)
        return score

def send_score(mqtt_client,score,score2):
    mqtt_client.send_message("received_score", [score,score2])

def find_pink_distance():
    robot = robo.Snatch3r()
    robot.pixy.mode = "SIG2"
    pink_x = robot.pixy.value(1)
    pink_y = robot.pixy.value(2)
    return pink_x


def find_green_distance():
    robot = robo.Snatch3r()
    robot.pixy.mode = "SIG1"
    green_x = robot.pixy.value(1)
    green_y = robot.pixy.value(2)
    green_width = robot.pixy.value(3)
    green_height = robot.pixy.value(4)
    return green_x

def find_green_height():
    robot = robo.Snatch3r()
    robot.pixy.mode = "SIG1"
    green_height = robot.pixy.value(4)
    return green_height





main()