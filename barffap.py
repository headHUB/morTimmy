#!/usr/bin/env python


class Robot:
    """ This class will hold the logic for our robot.
        It's name BaRfFaP stand for Building a Robot for Fun and Profit
        The brain of the robot is a raspberry Pi and the low level
        electronic are handled by an Arduino. The Arduino provides an
        interface to the DC motors and various sensors """

    def run(self):
        """ This function contains the main Robot loop """

        print "Hello World!"
        pass


def main():
    """ This is the main function of our script.
        It will only contain a very limited program
        logic. The main action happens in the Robot class """

    BaRfFap = Robot()
    BaRfFap.run()


if __name__ == '__main__':
    main()
