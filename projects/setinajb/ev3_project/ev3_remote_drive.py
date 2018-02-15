import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time


class MyDelegate(object):
    def __init__(self):
        pass


def main():
    robot = robo.Snatch3r()
    my_delegate = MyDelegate()
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
        if robot.color_sensor.color == ev3.ColorSensor.COLOR_RED:
            dp = 15
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        if dp != 0:
            mqtt_client.send_message("change_points", [dp])
            time.sleep(4)
            ev3.Leds.all_off()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()