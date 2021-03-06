#!/usr/bin/env python3
""""
This project demonstrates a robot that is capable of playing a modified version of "tag" with a human.
This file contains the code that is ran on the computer which allows the human to communicate with the robot
and vice-versa.

Author: Victoria Szalay
"""
import tkinter
from tkinter import ttk
import time
import mqtt_remote_method_calls as com


class TimeCount(object):
    """Helper class that stores information from tkinter box to use in separate function"""
    def __init__(self):
        self.entry_for_countdown = None
        self.label_for_countdown = None


class MyDelegateonThePC(object):
    """ Helper class that will receive MQTT messages from the EV3. """

    def __init__(self, label1_to_display_messages_in, label2_to_display_messages_in):
        self.display_label1 = label1_to_display_messages_in
        self.display_label2 = label2_to_display_messages_in

    def received_score(self, res1, res2):
        message_to_display = "Robot_score: {}".format(res1)
        self.display_label1.configure(text=message_to_display)
        another = "Human_score:{}".format(res2)
        self.display_label2.configure(text=another)


def main():
    """
    main() sets up the tkinter window and  calls necessary functions to send and receive information from
    the robot.
    """
    t = TimeCount()
    root = tkinter.Tk()
    root.title = 'Tag'

    frame = ttk.Frame(root, padding=20)
    frame.grid()

    entry = ttk.Entry(frame, width=8)
    entry.grid(row=2, column=4)
    t.entry_for_countdown = entry

    label = ttk.Label(frame, text='Put number in for countdown')
    label.grid(column=4, row=1)
    t.label_for_countdown = label

    label5 = ttk.Label(frame, text='Robot Tag')
    label5.grid(row=0, column=4)
    label2 = ttk.Label(frame, text='Whos It?')
    label2.grid(row=3, column=4)
    button1 = ttk.Button(frame, text="Human")
    button1.grid(row=3, column=3)
    button1["command"] = lambda: send_function_call(mqtt_client, 'run()', int(entry.get()), t)

    button2 = ttk.Button(frame, text="Robot")
    button2.grid(row=3, column=5)
    button2['command'] = lambda: send_function_call(mqtt_client, 'seek()', int(entry.get()), t)

    ev3_label = ttk.Label(frame, text='Score_Robot')
    ev3_label.grid(row=4, column=5)

    ev4_label = ttk.Label(frame, text='Score_Human')
    ev4_label.grid(row=4, column=3)

    pc_delegate = MyDelegateonThePC(ev3_label, ev4_label)
    mqtt_client = com.MqttClient(pc_delegate)
    mqtt_client.connect_to_ev3()

    root.mainloop()


def countdown(t):
    """
    :param t:
    :return: Nothing
    creates a countdown when called
    """
    entry = t.entry_for_countdown
    contents_of_entry_box = entry.get()
    num = float(contents_of_entry_box)
    while num:
        format_string = '{:0.2f} Time Left'
        answer = format_string.format(num)
        t.label_for_countdown['text'] = answer
        t.label_for_countdown.update()
        time.sleep(1)
        num -= 1
    t.label_for_countdown['text'] = "Times up!"
    print("Times up!")


def send_function_call(mqtt_client, function_call, t, input_time):
    print("Sending function = {}".format(function_call))
    print("Sending time = {}".format(t))
    mqtt_client.send_message("call_function", [function_call, t])
    countdown(input_time)


main()
