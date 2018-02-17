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
        self.count = 0
        self.count2 = 0

    def call_function(self, string_function_call,string_time_selected):
        print("Received: {}{} ".format(string_function_call,string_time_selected))
        if string_function_call == "seek()":
            self.n = seek(int(string_time_selected))
        elif string_function_call == "run()":
            self.m = run(int(string_time_selected))


def main():
    print("--------------------------------------------")
    print(" Robot Tag")
    print(" Press Back to exit when done.")
    print("--------------------------------------------")
    ev3.Sound.speak("Robot").wait()

    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()



    while my_delegate.running:
        if my_delegate.n > 0:
            send_score(mqtt_client,str(round(score(my_delegate))),str(round(score2(my_delegate))))
            my_delegate.n = 0
            time.sleep(0.01)
        if my_delegate.m >0:
            send_score(mqtt_client,str(round(score(my_delegate))),str(round(score2(my_delegate))))
            my_delegate.m = 0
            time.sleep(0.01)


def seek(time_alloted):
    start = time.time()
    """The robot is to find the person hiding."""
    robot = robo.Snatch3r()
    save = robot.seek_beacon()
    end = time.time()
    total = end - start
    if save == True:
        ev3.Sound.speak("I will catch you!")
        return  time_alloted - total



def run(time_alloted):
    """The robot is to randomly pick a path and follow it until time runs out to hide."""
    ev3.Sound.speak("I am looking for base!")
    robot = robo.Snatch3r()
    turn_speed = 100
    drive_speed = 300
    start = time.time()
    x= 3
    while x == 3:
        print("Pink Height",find_pink_height())
        print("Green Height",find_green_height())

        if find_pink_height() > 15:
            print("Pink height:", find_pink_height())
            robot.stop_motors()
            robot.turn_degrees(180, 400)
            robot.drive_forever(600, 600)
            time.sleep(.5)
            print("Pink!")
            ev3.Sound.speak("You cant catch me!")
        elif robot.touch_sensor.is_pressed:
            robot.stop_motors()
            end = time.time()
            total = end - start
            ev3.Sound.speak("I am caught")
            return time_alloted - total

        elif find_green_height() > 0:
            #robot.drive_inches(3,drive_speed)
            robot.drive_forever(drive_speed,drive_speed)
            if find_green_height()>150:
                robot.stop_motors()
                ev3.Sound.speak(("I am on base!"))
                return 1
        elif find_green_height() == 0:
            robot.drive_forever(turn_speed,-turn_speed)
        time.sleep(.01)
    ev3.Sound.speak("Out of time")
    return 0









def return_to_home():
    """The robot is to return to home base once return base button is pushed on pc"""
    start = time.time()
    robot = robo.Snatch3r
    robot.seek_beacon()
    end = time.time()
    total = end - start
    return total

def score(hi):
    hi.count = hi.count + hi.n
    return hi.count

def score2(hi):
    hi.count2 = hi.count2 + hi.m
    return hi.count2

def send_score(mqtt_client,score,score2):
    mqtt_client.send_message("received_score", [score,score2])

def find_pink_distance():
    robot = robo.Snatch3r()
    robot.pixy.mode = "SIG2"
    pink_x = robot.pixy.value(1)
    pink_y = robot.pixy.value(2)
    return pink_x

def find_pink_height():
    robot = robo.Snatch3r()
    robot.pixy.mode = "SIG2"
    pink_height = robot.pixy.value(4)
    pink_y = robot.pixy.value(2)
    return pink_height


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