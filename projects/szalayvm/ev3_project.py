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
    start = time.time()
    """The robot is to find the person hiding."""
    robot = robo.Snatch3r()
    drive_speed = 400
    total = 0
    #while total < time_alloted:
        #robot.seek_beacon()
        #end = time.time()
        #total = end - start
        #return total

    robot.pixy.mode = "SIG1"
    drive_speed = 400
    turn_speed = 200
    while not robot.touch_sensor.is_pressed:

        # Read the Pixy values for x and y
        # Print the values for x and y
        x = robot.pixy.value(1)
        y = robot.pixy.value(2)

        print("value1: X", x)

        if x < 150:
            robot.drive_forever(-turn_speed, turn_speed)
        elif x > 170:
            robot.drive_forever(turn_speed, -turn_speed)
        elif 150 <= x <= 170:
            robot.stop_motors()
            robot.drive_inches(8, turn_speed)
            if find_green_height() > 160:
                print("Hiding!")
                end = time.time()
                total = end - start
                return total

        time.sleep(0.25)

    end = time.time()
    print("Goodbye")
    total = start - end
    ev3.Sound.speak("You have found me!").wait()
    return total


def hide(time_alloted):
    """The robot is to randomly pick a path and follow it until time runs out to hide."""
    ev3.Sound.speak("I am hiding.")
    robot = robo.Snatch3r()
    turn_speed = 100
    drive_speed = 300
    start = time.time()

    while not robot.touch_sensor.is_pressed:
        print("Pink_distance", find_pink_distance())
        print("Green_height", find_green_height())
        if find_pink_height() > 15:
            print("Pink height:", find_pink_height())
            robot.stop_motors()
            robot.turn_degrees(180, 400)
            robot.drive_forever(600, 600)
            time.sleep(.5)
            print("Pink!")
        else:
            if find_green_height() > 0:
                #robot.drive_inches(3,drive_speed)
                robot.drive_forever(drive_speed,drive_speed)
                if find_green_height()>15:
                    robot.stop_motors()
                    time.sleep(.1)
                    ev3.Sound.speak("Hidden")
                    return 4
            elif find_green_height()==0:
                robot.drive_forever(turn_speed,-turn_speed)
            time.sleep(.25)
        end = time.time()
        total = end - start
        if robot.touch_sensor.is_pressed:
            ev3.Sound.speak("I am caught")
            robot.stop_motors()
            return total
        time.sleep(0.25)







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
    elif hi.n == 0:
        return 0

def score2(hi):
    if hi.m > hi.time:
        return 0
    elif hi.m <= hi.time:
        score = hi.time/(hi.m+1)
        return score
    elif hi.m == 0:
        return 0

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