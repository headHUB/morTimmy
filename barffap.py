#!/usr/bin/env python

# Motor ID definitions
FRONT_LEFT_MOTOR_ID = 1
FRONT_RIGHT_MOTOR_ID = 2
REAR_LEFT_MOTOR_ID = 3
REAR_RIGHT_MOTOR_ID = 4


class Robot:
    """ This class will hold the logic for our robot.
        It's name BaRfFaP stand for Building a Robot for Fun and Profit
        The brain of the robot is a raspberry Pi and the low level
        electronic are handled by an Arduino. The Arduino provides an
        interface to the DC motors and various sensors """

    def __init__(self,
                 frontLeftMotorID, frontRightMotorID,
                 rearLeftMotorID, rearRightMotorID):
        """ This function initialises our robot.
            It only requires the various motor IDs for now """

        self.frontLeftMotorID = frontLeftMotorID
        self.frontRightMotorID = frontRightMotorID
        self.rearLeftMotorID = rearLeftMotorID
        self.rearRightMotorID = rearRightMotorID


    def run(self):
        """ This function contains the main Robot loop """

        print "Hello World!"


def main():
    """ This is the main function of our script.
        It will only contain a very limited program
        logic. The main action happens in the Robot class """

    BaRfFap = Robot(FRONT_LEFT_MOTOR_ID, 
                    FRONT_RIGHT_MOTOR_ID,
                    REAR_LEFT_MOTOR_ID,
                    REAR_RIGHT_MOTOR_ID)
    BaRfFap.run()


if __name__ == '__main__':
    main()
