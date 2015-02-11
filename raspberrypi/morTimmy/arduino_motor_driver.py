#!/usr/bin/env python

from motor_driver import MotorDriver


class Motor(MotorDriver):
    """ This class is a child of the generic driver for DC Motors.
    It will contain the class for working together with the
    DC Motors connected to the arduino through the H-Bridge modules.

    The H-Bridge module allows you to control motors in both
    directions.

    Interface will be handled through a serial
    connection between the raspberry pi and the arduino.

    (TODO, write arduino serial remote control library)
    """

    def __init__(self, motorID):
        """ The intialisator requires the ID of the motor """
        self.ID = motorID
        self.currentSpeed = 0

    def setSpeed(self, speed):
        """ This function will be used to set the speed of the motor

        Args:
          speed (int): sets the speed of the motor. Valid values are
          between -255 and 255. Negative numbers will put the motor
          in reverse. Zero will stop the motor
        """
        self.currentSpeed = speed

    def getSpeed(self):
        """ This function will return the current speed of the motor """

        return self.currentSpeed


def main():
    """ This function will only be called when the library is run
    directly Only to be used to do quick tests on the library
    """

    print ("Hello World! This is the library for controlling DC motors "
           "through the Arduino")

    motor = Motor(1)
    motor.setSpeed(255)
    print "Motor #%d speed is %d" % (motor.ID, motor.getSpeed())
    motor.setSpeed(-255)
    print "Motor #%d speed is %d" % (motor.ID, motor.getSpeed())

if __name__ == '__main__':
    main()
