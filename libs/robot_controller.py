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


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    def __init__(self):
        """ Constructs all necessary initial instance variables for the snatch3r class."""
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        assert self.left_motor
        assert self.right_motor

    def drive_inches(self, inches_to_target, speed_degrees):
        """ Takes in inches needed for travel and speed at which to travel and makes robot move that distance at that speed.
        Input: inches_to_target (int), speedDegrees(int)
        Output: None
        """
        degree_to_inch = 90
        deg = inches_to_target * degree_to_inch

        self.left_motor.run_to_rel_pos(speed_sp=speed_degrees, position_sp=deg, stop_action='brake')
        self.right_motor.run_to_rel_pos(speed_sp=speed_degrees, position_sp=deg, stop_action='brake')
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self,degrees_to_turn, turn_speed_sp):
        """ Takes in degrees you want the robot to turn and the speed at which the robot should complete the turns.
          Input: degrees_to_turn(int), turn_speed_sp(int)
          Output: None
          Side Effects: None
          """
        if degrees_to_turn > 0:
            self.left_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=-degrees_to_turn*5, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
            self.right_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=degrees_to_turn*5, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        else:
            self.left_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=degrees_to_turn*5, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
            self.right_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=-degrees_to_turn*5, stop_action=ev3.Motor.STOP_ACTION_BRAKE)