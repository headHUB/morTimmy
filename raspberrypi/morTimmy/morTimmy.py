#!/usr/bin/env python

# imports
from arduino_serial_hardware_control import ArduinoSerialController
from bluetooth_remote_control import RemoteController


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

    arduino = HardwareController()
    remoteControl = RemoteController()

    def __init__(self):
        """ Called when the robot class is created.

        At the moment we only launch into the self.initialize()
        function

        Args:

        Returns:
          The function doesn't explicitly return anything. Python
          defaults to return None in this case

        Raises:
          TODO: Add proper error handling.
        """
        self.initialize()

    def initialize(self):
        """ (re)initializes the robot.

        We have this in a seperate function (opposed to __init__)
        so we can easily reinitialise the robot within our class
        """
        pass

    def run(self):
        """ The main robot loop """

        remoteRecvCommand = self.remoteControl.recvCommand()

        arduinoRecvCommand = self.arduino.recvCommand()
        if arduinoRecvCommand:
            print arduinoRecvCommand
            if '200' in arduinoRecvCommand:
                self.arduino.sendCommand(self.commands['goForward'])
            else:
                self.arduino.sendCommand(self.commands['goBack'])


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
