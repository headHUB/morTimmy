#!/usr/bin/env python

# imports
from arduino_motor_driver import Motor
from arduino_serial_hardware_control import ArduinoSerialController

# Motor ID definitions
FRONT_LEFT_MOTOR_ID = 1
FRONT_RIGHT_MOTOR_ID = 2
REAR_LEFT_MOTOR_ID = 3
REAR_RIGHT_MOTOR_ID = 4


class Robot:
    """ Main class for controlling our robot morTimmy

    The brain of the robot is a raspberry Pi and the low level
    electronic are handled by an Arduino. The Arduino provides
    an interface to the DC motors and various sensors
    """

    commands = {'goForward': 'W',
                'goBack': 'S',
                'goLeft': 'A',
                'goRight': 'D'}

    arduino = ArduinoSerialController()

    def __init__(self, frontLeftMotorID, frontRightMotorID,
                 rearLeftMotorID, rearRightMotorID):
        """ Called when the robot class is created.

        At the moment we only launch into the self.initialize()
        function

        Args:
          frontLeftMotorID (int): Motor ID of the front left DC
            motor
          frontRightMotorID (int): Motor ID of the front right
            DC motor
          rearLeftMotorID (int): Motor ID of the rear left DC
            motor
          rearRightMotorID (int): Motor ID of the rear right
            DC motor

        Returns:
          The function doesn't explicitly return anything. Python
          defaults to return None in this case

        Raises:
          TODO: Add proper error handling.
        """
        self.frontLeftMotor = Motor(frontLeftMotorID)
        self.frontRightMotor = Motor(frontRightMotorID)
        self.rearLeftMotor = Motor(rearLeftMotorID)
        self.rearRightMotor = Motor(rearRightMotorID)

        self.initialize()

    def initialize(self):
        """ (re)initializes the robot.

        We have this in a seperate function (opposed to __init__)
        so we can easily reinitialise the robot within our class
        """
        pass

    def run(self):
        """ The main robot loop """

        recvCommand = self.arduino.recvCommand()
        if recvCommand:
            print recvCommand
            if '200' in recvCommand:
                self.arduino.sendCommand(self.commands['goForward'])
            else:
                self.arduino.sendCommand(self.commands['goBack'])


def main():
    """ This is the main function of our script.

    It will only contain a very limited program
    logic. The main action happens in the Robot class
    """
    morTimmy = Robot(FRONT_LEFT_MOTOR_ID,
                     FRONT_RIGHT_MOTOR_ID,
                     REAR_LEFT_MOTOR_ID,
                     REAR_RIGHT_MOTOR_ID)

    try:
        while(True):
            morTimmy.run()
    except KeyboardInterrupt:
        print "Thanks for running me!"

if __name__ == '__main__':
    main()
