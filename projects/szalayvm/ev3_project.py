#!/usr/bin/env python3
""""
This project demonstrates a robot that is capable of playing a modified version of "tag" with a human.
This file contains the code that is uploaded and ran on the robot, and is used to send back information
to the computer.
It has two  main functions:
seek(): finds the human using the IR sensor
run(): finds "base" with the pixy cam and runs from the human, who is a distinct color from the base.

Author: Victoria Szalay
"""

import robot_controller as robo

import time
import ev3dev.ev3 as ev3
import mqtt_remote_method_calls as com
import math


class MyDelegate(object):
    """helper class receives function calls from PC"""

    def __init__(self):
        self.running = True
        self.robot = 0
        self.human = 0
        self.count = 0
        self.count2 = 0

    def call_function(self, string_function_call, string_time_selected):
        print("Received: {}{} ".format(string_function_call, string_time_selected))
        if string_function_call == "seek()":
            self.robot = seek(int(string_time_selected))
        elif string_function_call == "run()":
            self.human = run(int(string_time_selected))


def main():
    print("--------------------------------------------")
    print(" Robot Tag")
    print("--------------------------------------------")
    ev3.Sound.speak("Robot Tag").wait()

    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()

    while my_delegate.running:
        if my_delegate.n > 0 or my_delegate.m > 0:
            send_score(mqtt_client, str(round(robot_score(my_delegate))), str(round(human_score(my_delegate))))
            my_delegate.n = 0
            my_delegate.m = 0
            time.sleep(0.01)


def seek(time_alloted):
    """The robot is to find the person hiding by seeking the IR. If the alloted time(received from the
    GUI on the PC program, runs out, then this function returns a penalty point of 1. If the human is found,
    then the robot sends back a score that is the difference between the time alloted and the time it took
    to find the human."""
    start = time.time()
    robot = robo.Snatch3r()
    beacon_seeker = ev3.BeaconSeeker(channel=1)

    forward_speed = 300
    turn_speed = 100

    while time_alloted > time.time() - start:
        current_heading = beacon_seeker.heading
        current_distance = beacon_seeker.distance
        if current_distance == -128:
            print("IR Remote not found. Distance is -128")
            robot.drive_forever(-1 * turn_speed, turn_speed)
        else:
            if math.fabs(current_heading) < 2:
                print("On the right heading. Distance: ", current_distance)
                if current_distance == 1:
                    robot.drive_inches(4, 300)
                    robot.stop_motors()
                    ev3.Sound.speak("Tag")
                    end = time.time()
                    total = end - start
                    return time_alloted - total
                if current_distance > 1:
                    robot.drive_forever(forward_speed, forward_speed)
            if 2 < math.fabs(current_heading) < 10:
                print("Adjusting heading:", current_heading)
                if current_heading < 0:
                    robot.drive_forever(-1 * turn_speed, turn_speed)
                if current_heading > 0:
                    robot.drive_forever(turn_speed, -1 * turn_speed)
            if math.fabs(current_heading) > 10:
                print("Heading is too far off to fix", current_heading)
                robot.drive_forever(-1 * turn_speed, turn_speed)

        time.sleep(0.2)

    robot.stop_motors()
    ev3.Sound.speak("Ran out of time")
    return 1


def run(time_alloted):
    """
    The robot is to seek a green_colored base, but if a human wearing pink is spotted, then the robot is to
    run away. The human receives a default point of 1 if the robot reaches base or a score computed
    from time alloted.
    """
    ev3.Sound.speak("I am looking for base!")
    robot = robo.Snatch3r()
    turn_speed = 100
    drive_speed = 300
    start = time.time()
    start_loop = 3
    while start_loop == 3:
        print("Pink Height", find_pink_height())
        print("Green Height", find_green_height())

        if find_pink_height() > 15:
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
            robot.drive_forever(drive_speed, drive_speed)
            if find_green_height() > 150:
                robot.stop_motors()
                ev3.Sound.speak('I am on base!')
                return 1
        elif find_green_height() == 0:
            robot.drive_forever(turn_speed, -turn_speed)
        time.sleep(.01)
    ev3.Sound.speak("Out of time")
    return 0


def robot_score(mydelegate):
    """
    :param mydelegate:
    :return: score calculated from seek() function
    """
    mydelegate.count = mydelegate.count + mydelegate.robot
    return mydelegate.count


def human_score(mydelegate):
    """
    :param mydelegate:
    :return: score calculated from hide() function
    """
    mydelegate.count2 = mydelegate.count2 + mydelegate.human
    return mydelegate.count2


def send_score(mqtt_client, robot_score, human_score):
    """
    :param mqtt_client:
    :param robot_score:
    :param human_score:
    :return: Nothing
    """
    mqtt_client.send_message("received_score", [robot_score, human_score])


def find_pink_height():
    """
    :return: returns height read from SIG2 on pixy cam
    """
    robot = robo.Snatch3r()
    robot.pixy.mode = "SIG2"
    pink_height = robot.pixy.value(4)
    return pink_height


def find_green_height():
    """
    :return: returns height read from SIG1 on pixy cam
    """
    robot = robo.Snatch3r()
    robot.pixy.mode = "SIG1"
    green_height = robot.pixy.value(4)
    return green_height


main()
