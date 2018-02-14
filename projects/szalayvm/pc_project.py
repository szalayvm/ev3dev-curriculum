import tkinter
from tkinter import ttk

def main():
    root = tkinter.Tk()

    frame = ttk.Frame(root, padding=20)
    frame.grid()

    label = ttk.Label(frame, text='Three Wishes')
    label.grid()

    root.mainloop()

main()