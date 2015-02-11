#!/usr/bin/env python


class MotorDriver():
    """ Generic driver for DC Motors.

    It will contain the basic skeleton for working with DC motors.

    Specific child classes will be created based on this class
    for different types of motors in the project.
    """

    def setSpeed(self, speed):
        """ Used to set the speed and direction of the motor

        Args:
          speed (int): Sets the speed of the motor. Negative numbers
          put the motor in reverse, zero will stop the motor. valid
          values are between -255 and 255.
        """

        pass

    def getSpeed(self):
        """ This function will return the current speed of the motor """
        pass


def main():
    """ This function will only be called when the library is run directly
    Only to be used to do quick tests on the library.
    """

    print "Hello World, this is the generic motor driver library"

if __name__ == '__main__':
    main()
