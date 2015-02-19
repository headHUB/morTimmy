#!/usr/bin/env python

# imports
from hardware_controller import *
from time import sleep
import Queue


class Robot:
    """ Main class for controlling our robot morTimmy

    The brain of the robot is a raspberry Pi and the low level
    electronic are handled by an Arduino. The Arduino provides
    an interface to the DC motors and various sensors
    """

    arduino = HardwareController()
    runningTime = 0
    isRunning = False
    isStopped = True

    def __init__(self):
        """ Called when the robot class is created.

        At the moment we only launch into the self.initialize()
        function.

        Returns:

        Raises:
          TODO: Add proper error handling.
        """

        self.sensorDataQueue = Queue.Queue()
        self.initialize()

    def initialize(self):
        """ (re)initializes the robot.

        Responsible for setting up the connection to the Arduino.
        The function loops until a connection is established
        """
        while not self.arduino.isConnected:
            print ("Failed to establish connection to Arduino, retrying in 5s")
            sleep(5)                # wait 5sec before trying again
            self.arduino.initialize()

    def run(self):
        """ The main robot loop """

        currentTime = time.time()
        deltaTime = self.runningTime - currentTime

        # Check connection to arduino, reinitialize if not
        if not self.arduino.isConnected:
            self.arduino.initialize()

        # Move robot forward if stopped for 5sec
        if self.isStopped and deltaTime >= 5:
            self.arduino.sendMessage(MODULE_MOTOR, CMD_MOTOR_FORWARD, '255')
            self.runningTime = currentTime
            self.isRunning = True
        # Stop robot if running for 5sec
        elif self.isRunning and deltaTime >= 5:
            self.arduino.sendMessage(MODULE_MOTOR, CMD_MOTOR_STOP)
            self.runningTime = currentTime
            self.isStopped = True

        # Process all received messages in the queue
        while not self.arduino.recvMessageQueue.empty():
            recvMessage = self.recvMessageQueue.get_nowait()

            if recvMessage == 'Invalid':
                print "LOG: received invalid packet, ignoring"
                pass
            elif recvMessage['module'] == MODULE_DISTANCE_SENSOR:
                self.sensorDataQueue.put(recvMessage['data'])
            elif recvMessage['module'] == MODULE_MOTOR:
                if recvMessage['commandType'] == CMD_MOTOR_FORWARD_NACK:
                    print ("Error moving forward, resending command")
                    self.arduino.sendMessage(MODULE_MOTOR,
                                             CMD_MOTOR_FORWARD,
                                             '255')
                elif recvMessage['commandType'] == CMD_MOTOR_BACK_NACK:
                    pass
                elif recvMessage['commandType'] == CMD_MOTOR_LEFT_NACK:
                    pass
                elif recvMessage['commandType'] == CMD_MOTOR_RIGHT_NACK:
                    pass
                else:
                    print "Unknown %d cmd %d" % (recvMessage['module'],
                                                 recvMessage['commandType'])


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
