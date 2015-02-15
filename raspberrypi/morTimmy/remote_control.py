#!/usr/bin/env python

class ControllerDriver:
    """ Generic class for remote controlling morTimmy the Robot
    
    It will be used to control the Arduino microcontroller to
    perform various low level functions like driving and reading
    sensor data.

    This class will also be used to control the Raspberry Pi
    using external remote controls like a game controller or 
    bluetooth phone application
    """

class ControllerCmd:
    """ Command definition for controller drivers

    This class defines the various commands our robot morTimmy
    can respond to. It's used by both the arduino/raspberry pi
    interface and remote control devices interfacing with the 
    Raspberry Pi.
    """

    int leftMotorSpeed       # Controls the speed of the left side motors
    int rightMotorSpeed      # Controls the speed of the right side motors

    def goForward(speed):
        leftMotorSpeed = speed
        rightMotorSpeed = speed

    def goBack(speed):
        leftMotorSpeed = -speed
        rightMotorSpeed = -speed

    def goLeft(speed):
        leftMotorSpeed = -speed
        rightMotorSpeed = speed

    def goRight(speed):
        leftMotorSpeed = speed
        rightMotorSpeed = -speed

    def stop():
        leftMotorSpeed = 0
        rightMotorSpeed = 0

    def joystick(int x, int y):
        """ Controlling the robot using a joystick 

        Args:
            x (int): x-axis of the joystick, controls the amount of
                     steering
            y (int): y-axis if the joystick, controls the
                     forward/back speed
        """
        leftMotorSpeed = x - y;
        rightMotorSpeed = x + y;

        # Make sure the remote control x and y values
        # do not exceed the maximum speed
        if (leftMotorSpeed < -255)
            leftMotorSpeed = -255;
        else if (leftMotorSpeed > 255)
            leftMotorSpeed = 255;
        if (rightMotorSpeed < -255)
            rightMotorSpeed = -255;
        else if (rightMotorSpeed > 255)
            rightMotorSpeed = 255;


def main():
    pass

if __name__ == '__main__':
    main()
