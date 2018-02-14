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
import robot_controller as robo

robot = robo.Snatch3r()

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

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    left_button['command'] = lambda: print("Left button")
    root.bind('<Left>', lambda event: print("Left key"))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    stop_button['command'] = lambda: print("Stop button")
    root.bind('<space>', lambda event: print("Stop key"))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    right_button['command'] = lambda: print("Right button")
    root.bind('<Right>', lambda event: print("Right key"))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    back_button['command'] = lambda: print("Back button")
    root.bind('<Down>', lambda event: print("Back key"))


    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = lambda: print("Quit button")

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = lambda: exit()

    root.mainloop()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()

