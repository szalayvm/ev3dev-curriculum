import tkinter
from tkinter import ttk
import time

class time_count(object):
    def __init__(self):
        self.entry_for_countdown = None
        self.label_for_countdown = None

def main():
   interface()

def interface():
    t = time_count()
    root = tkinter.Tk()
    root.title = 'Hide&Seek'

    frame = ttk.Frame(root, padding=20)
    frame.grid()

    entry = ttk.Entry(frame, width=8)
    entry.grid(row=1, column=0)
    t.entry_for_countdown = entry

    label = ttk.Label(frame, text='Put number in for countdown')
    label.grid()
    t.label_for_countdown = label

    button3 = ttk.Button(frame, text="Start Countdown")
    button3.grid()
    button3['command'] = lambda: countdown(t)

    label5 = ttk.Label(frame, text='Hide&Seek')
    label5.grid(row=0, column=2)
    label2 = ttk.Label(frame, text='Whos It?')
    label2.grid(row=2, column=4)
    button1 = ttk.Button(frame, text="Human")
    button1.grid(row=3, column=3)

    button2 = ttk.Button(frame, text="Robot")
    button2.grid(row=3, column=5)

    root.mainloop()

def countdown(t):
    entry = t.entry_for_countdown
    contents_of_entry_box = entry.get()
    num = float(contents_of_entry_box)
    while num:
        format_string = '{:0.2f} Time Left'
        answer = format_string.format(num)
        t.label_for_countdown['text'] = answer
        t.label_for_countdown.update()
        print(num)
        time.sleep(1)
        num -= 1
    t.label_for_countdown['text'] = "Times up!"
    print("Times up!")



main()