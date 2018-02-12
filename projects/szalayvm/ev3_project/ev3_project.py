#!/usr/bin/env python3
""""
Contains final project code for CSSE120.
Author: Victoria Szalay
"""
import tkinter
from tkinter import ttk

def main():
    root = tkinter.Tk()

    frame = ttk.Frame(root,padding=20)
    frame.grid()

    label = ttk.Label(frame, text='Three Wishes')
    label.grid()

    root.mainloop()

def first_wish():
    """The robot is to make the wisher famous by posting to twitter."""
main()