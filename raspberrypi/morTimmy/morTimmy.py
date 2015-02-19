#!/usr/bin/env python

# imports
from hardware_controller import *
from time import sleep


class Robot:
    """ Main class for controlling our robot morTimmy

    The brain of the robot is a raspberry Pi and the low level
    electronic are handled by an Arduino. The Arduino provides
    an interface to the DC motors and various sensors
    """

    arduino = HardwareController()

    def __init__(self):
        """ Called when the robot class is created.

        At the moment we only launch into the self.initialize()
        function.

        Returns:

        Raises:
          TODO: Add proper error handling.
        """
        self.initialize()

    def initialize(self):
        """ (re)initializes the robot.

        Responsible for setting up the connection to the Arduino.
        The function loops until a connection is established
        """
        self.arduino.initialize()

    def run(self):
        """ The main robot loop """

        if self.arduino.isConnected:
            self.arduino.sendMessage(MODULE_MOTOR, CMD_MOTOR_FORWARD,
                                     'Data for my Arduino friend')
            self.arduino.recvMessage()
        else:
            while not self.arduino.isConnected:
                print ("Failed to establish connection to Arduino, "
                       "retrying in 5s")
                sleep(5)                # wait 5sec before trying again
                self.arduino.initialize()


def main():
    """ This is the main function of our script.

    It will only contain a very limited program
    logic. The main action happens in the Robot class
    """
    morTimmy = Robot()

    try:
        while(True):
            morTimmy.run()
    except KeyboardInterrupt:
        print "Thanks for running me!"

if __name__ == '__main__':
    main()
