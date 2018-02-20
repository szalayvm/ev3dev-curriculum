import mqtt_remote_method_calls as com
from robot_controller import Snatch3r as Snatch3r
import ev3dev.ev3 as ev3
import time

#


class MyDelegate(object):
    def __init__(self, robot):
        """

        :param robot: robot.Snatch3r
        """
        self.robot = robot

    def drive_forever(self, left_speed, right_speed):
        print('told to drive at', left_speed, right_speed)
        self.robot.drive_forever(left_speed, right_speed)

    def stop_motors(self):
        print('told to stop')
        self.robot.left_motor.stop()
        self.robot.right_motor.stop()


def main():
    print("Running")
    robot = Snatch3r()
    my_delegate = MyDelegate(robot)
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()

    while True:
        dp = 0
        ev3.Leds.all_off()
        if robot.color_sensor.color == ev3.ColorSensor.COLOR_RED:
            print("Hit red")
            dp = 15
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        elif robot.color_sensor.color == ev3.ColorSensor.COLOR_YELLOW:
            print("Hit yellow")
            dp = -10
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
        elif robot.color_sensor.color == ev3.ColorSensor.COLOR_BLUE:
            print("Hit blue")
            dp = -5
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
            robot.turn_degrees(380, 900)


        if dp != 0:
            mqtt_client.send_message("change_points", [dp])
            # time.sleep(4)
            ev3.Leds.all_off()
        time.sleep(0.05)


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()