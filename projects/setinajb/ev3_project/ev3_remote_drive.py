import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time

#


class MyDelegate(object):
    def __init__(self, robot):
        self.robot = robot

    def drive_forever(self, left_speed, right_speed):
        print('told to drive at', left_speed, right_speed)
        self.robot.drive_forever(left_speed, right_speed)

    def stop_motors(self):
        print('told to stop')
        self.robot.drive_forever(0, 0)


def main():
    print("Running")
    robot = robo.Snatch3r()
    my_delegate = MyDelegate(robot)
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()

    while True:
        dp = 0
        if robot.color_sensor.color == ev3.ColorSensor.COLOR_YELLOW:
            dp = -10
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
        if robot.color_sensor.color == ev3.ColorSensor.COLOR_BLUE:
            dp = -5
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
            robot.turn_degrees(360, 900)
        if robot.color_sensor.color == ev3.ColorSensor.COLOR_RED:
            dp = 15
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        if dp != 0:
            mqtt_client.send_message("change_points", [dp])
            time.sleep(4)
            ev3.Leds.all_off()
        time.sleep(0.1)


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()