#!/usr/bin/env python3
"""
This module will drive the ev3 robot using the commands the user specifies on the tkinter window.

Author: Jaclyn Setina."""

import tkinter
from tkinter import ttk
from tkinter import *
import random
import ev3dev.ev3 as ev3
import time
import mqtt_remote_method_calls as com


def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=50)
    main_frame.grid()  # only grid call that does NOT need a row and column

    photo = PhotoImage(file="mariokart.png")
    label = Label(main_frame, image=photo)
    label.grid(row=0, column=1)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    forward_button['command'] = lambda: print("Forward button")
    forward_button['command'] = lambda: handle_forward(mqtt_client, 900, 900)

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    left_button['command'] = lambda: print("Left button")
    left_button['command'] = lambda: handle_left(mqtt_client, 900, 900)

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    stop_button['command'] = lambda: print("Stop button")
    stop_button['command'] = lambda: handle_stop(mqtt_client)

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    right_button['command'] = lambda: print("Right button")
    right_button['command'] = lambda: handle_right(mqtt_client, 900, 900)

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    back_button['command'] = lambda: print("Back button")
    back_button['command'] = lambda: handle_back(mqtt_client, 900, 900)

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = lambda: print("Quit button")

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = lambda: exit()


    root.mainloop()

# ----------------------------------------------------------------------
# Tkinter callbacks
# ----------------------------------------------------------------------


def handle_forward(mqtt_client, left_speed, right_speed):
    mqtt_client.send_message('drive_forever', [900, 900])


def handle_left(mqtt_client, left_speed, right_speed):
    mqtt_client.send_message('drive_forever', [-1*900, 900])


def handle_stop(mqtt_client):
    mqtt_client.send_message('stop_motors')


def handle_right(mqtt_client, left_speed, right_speed):
    mqtt_client.send_message('drive_forever', [900, -1*900])


def handle_back(mqtt_client, left_speed, right_speed):
    mqtt_client.send_message('drive_forever', [-1*900, -1*900])


# Quick and exit
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()

