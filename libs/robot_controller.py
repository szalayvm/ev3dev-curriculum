"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    def __init__(self):
        """ Constructs all necessary initial instance variables for the snatch3r class."""
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.MAX_SPEED = 900
        self.touch_sensor = ev3.TouchSensor()
        self.LED = ev3.Leds
        assert self.left_motor
        assert self.right_motor
        assert self.arm_motor

    def drive_inches(self, inches_to_target, speed_deg):
        """ Takes in inches needed for travel and speed at which to travel and makes robot move that distance at that speed.
        Input: inches_to_target (int), speedDegrees(int)
        Output: None
        """
        degree_to_inch = 90
        deg = inches_to_target * degree_to_inch

        self.left_motor.run_to_rel_pos(speed_sp=speed_deg, position_sp=deg, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.run_to_rel_pos(speed_sp=speed_deg, position_sp=deg, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        """ Takes in degrees you want the robot to turn and the speed at which the robot should complete the turns.
          Input: degrees_to_turn(int), turn_speed_sp(int)
          Output: None
          Side Effects: None
          """
        brake = ev3.Motor.STOP_ACTION_BRAKE
        if degrees_to_turn > 0:
            self.left_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=-degrees_to_turn*5, stop_action=brake)
            self.right_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=degrees_to_turn*5, stop_action=brake)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_up(self):
        """ Makes the robot put its arm all the way up
         Input: None
         Output: An audible Beep"""
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

    def arm_calibration(self):
        """ Makes the robot move its arm up and down with beeps in between
         Input: None
         Output: None """
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)

        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

        rev_to_position = 14.2 * 360
        self.arm_motor.run_to_rel_pos(position_sp=-rev_to_position)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

        self.arm_motor.position = 0  # Calibrate the down position as 0 (this line is correct as is).

    def arm_down(self):
        """ Makes the robot put its arm down
         Input: None
         Output: None """
        self.arm_motor.run_to_abs_pos()
        self.arm_motor.wait_while(ev3.Motor.STATE_HOLDING)  # Blocks until the motor finishes running

        rev_to_position = 14.2 * 360
        self.arm_motor.run_to_rel_pos(position_sp=-rev_to_position)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def loop_forever(self):
        # This is a convenience method that I don't really recommend for most programs other than m5.
        #   This method is only useful if the only input to the robot is coming via mqtt.
        #   MQTT messages will still call methods, but no other input or output happens.
        # This method is given here since the concept might be confusing.
        self.running = True
        while self.running:
            time.sleep(0.1)  # Do nothing (except receive MQTT messages) until an MQTT message calls shutdown.

    def shutdown(self):
        """ Shuts the robot down
         Input: None
         Output: Prints goodbye, beeps out goodbye """
        self.left_motor.stop()
        self.right_motor.stop()
        self.LED.set_color(self.LED.LEFT, self.LED.GREEN)
        self.LED.set_color(self.LED.RIGHT, self.LED.GREEN)
        print('goodbye')
        ev3.Sound.speak('Goodbye').wait()
