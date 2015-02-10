#!/usr/bin/env python

# imports
from arduino_motor_driver import Motor

# Motor ID definitions
FRONT_LEFT_MOTOR_ID = 1
FRONT_RIGHT_MOTOR_ID = 2
REAR_LEFT_MOTOR_ID = 3
REAR_RIGHT_MOTOR_ID = 4


class Robot:
    """ This class will hold the logic for our robot morTimmy.
        The brain of the robot is a raspberry Pi and the low level
        electronic are handled by an Arduino. The Arduino provides
        an interface to the DC motors and various sensors
    """

    def __init__(self, frontLeftMotorID, frontRightMotorID,
                 rearLeftMotorID, rearRightMotorID):
        """ This function initialises our robot.
            It only requires the various motor IDs for now
        """

        self.frontLeftMotor = Motor(frontLeftMotorID)
        self.frontRightMotor = Motor(frontRightMotorID)
        self.rearLeftMotor = Motor(rearLeftMotorID)
        self.rearRightMotor = Motor(rearRightMotorID)

    def run(self):
        """ This function contains the main robot loop
            as an initial test we're going to get the
            robot to spin constantly
        """

        print "The (hello) world keeps spinning!!"
        self.frontLeftMotor.setSpeed(255)
        self.frontRightMotor.setSpeed(-255)
        self.rearLeftMotor.setSpeed(255)
        self.rearRightMotor.setSpeed(-255)


def main():
    """ This is the main function of our script.
        It will only contain a very limited program
        logic. The main action happens in the Robot class
    """

    morTimmy = Robot(FRONT_LEFT_MOTOR_ID,
                     FRONT_RIGHT_MOTOR_ID,
                     REAR_LEFT_MOTOR_ID,
                     REAR_RIGHT_MOTOR_ID)
    morTimmy.run()


if __name__ == '__main__':
    main()
