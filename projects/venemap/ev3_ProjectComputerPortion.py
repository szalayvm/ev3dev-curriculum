import tkinter
from tkinter import ttk
import rosegraphics as rg
import math
import time
import mqtt_remote_method_calls as com

class MyDelegate(object):

    def __init__(self, canvas):
        self.canvas = canvas
        self.driveLocations = []
        self.driveDirectionVectors = [(0, 1)]
        self.deltaX = 0
        self.deltaY = 0
        self.length = 0
        self.lengths = []
    def on_circle_draw(self, color, x, y):
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, width=2)
        self.driveLocations += [rg.Point(x, y)]
        a = self.driveLocations
        if len(self.driveLocations) > 1:
            self.deltaX = a[len(a) - 1].x - a[len(a) - 2].x
            self.deltaY = -1 * (a[len(a) - 1].y - a[len(a) - 2].y)
            self.length = math.sqrt(self.deltaX**2 + self.deltaY**2)
            print(self.deltaX, self.deltaY)
            if self.length != 0:
                self.driveDirectionVectors += [(self.deltaX / self.length, self.deltaY / (self.length))]
                self.canvas.create_line(a[len(a)-1].x, a[len(a)-1].y, a[len(a)-2].x, a[len(a)-2].y)
                self.lengths += [self.length]


class MyDelegateOnThePc(object):
    """ Helper class that will receive MQTT messages from the EV3. """

    def __init__(self, score_label, start_points):
        self.display_label = score_label
        self.points = start_points

    def change_points(self, diff_points):
        self.points = self.points + diff_points
        # print("Received: ", diff_points)
        message_to_display = "{} points.".format(self.points)
        # self.display_label.configure(text=message_to_display)
        self.display_label["text"] = message_to_display


def main():
    root = tkinter.Tk()
    root.title = "Waypoint"

    main_frame = ttk.Frame(root, padding=5)
    main_frame.grid()

    instructions = "Click to set waypoints to drive to"
    label = ttk.Label(main_frame, text=instructions)
    label.grid(columnspan=3)

    # Make a tkinter.Canvas on a Frame.
    canvas = tkinter.Canvas(main_frame, background="lightgray", width=400, height=300)
    canvas.grid(columnspan=3)
    # Make callbacks for mouse click events.
    canvas.bind("<Button-1>", lambda event: left_mouse_click(event, my_delegate))

    # Make callbacks for the two buttons.
    clear_button = ttk.Button(main_frame, text="Clear")
    clear_button.grid(row=3, column=0)
    clear_button["command"] = lambda: clear(canvas, my_delegate)

    # testButton = ttk.Button(main_frame, text="testArray")
    # testButton.grid(row=3,column=4)
    # testButton['command'] = lambda: print(my_delegate.driveLocations, my_delegate.lengths)

    quit_button = ttk.Button(main_frame, text="Quit")
    quit_button.grid(row=3, column=2)
    quit_button["command"] = lambda: quit_program(mqtt_client)

    beginDrive = ttk.Button(main_frame, text="Drive")
    beginDrive.grid(row=3, column=1)
    beginDrive["command"] = lambda: beginDriving(mqtt_client, my_delegate.driveLocations, my_delegate.driveDirectionVectors, my_delegate.lengths)

    # Create a score label
    score_label = ttk.Label(main_frame, text="0 points")
    score_label.grid(row=5, column=1)

    # Create an MQTT connection
    # Done: 5. Delete the line below (mqtt_client = None) then uncomment the code below.  It creates a real mqtt client.
    my_delegate = MyDelegate(canvas)
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()
    # mqtt_client.connect('draw', 'draw')

    score_delegate = MyDelegateOnThePc(score_label, 0)
    mqtt_client2 = com.MqttClient(score_delegate)
    mqtt_client2.connect_to_ev3()

    root.mainloop()
# ----------------------------------------------------------------------
# Tkinter event handlers
# Left mouse click
# ----------------------------------------------------------------------
def left_mouse_click(event, myDelegate):
    my_color = "navy"
    myDelegate.on_circle_draw(my_color, event.x, event.y)

def clear(canvas, myDelegate):
    """Clears the canvas contents"""
    canvas.delete("all")
    myDelegate.driveLocations = []
    myDelegate.driveDirectionVectors = [(0,1)]


def quit_program(mqtt_client):
    """For best practice you should close the connection.  Nothing really "bad" happens if you
       forget to close the connection though. Still it seems wise to close it then exit."""
    if mqtt_client:
        mqtt_client.close()
    exit()


def beginDriving(mqtt_client, driveLocations, driveVectors, lengths):
    for k in range(1, len(driveLocations), 1):
        turn_amount = math.acos(driveVectors[k-1][0] * driveVectors[k][0] + driveVectors[k-1][1] * driveVectors[k][1])*180/math.pi
        if driveVectors[k][0] > 0:
            turn_amount = -turn_amount
        print('turn amt', turn_amount)
        mqtt_client.send_message("turn_degrees", [turn_amount, 400])
        driveLength = lengths[k-1] * .1
        mqtt_client.send_message("drive_inches", [driveLength, 400])


main()
