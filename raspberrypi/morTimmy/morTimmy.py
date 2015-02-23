#!/usr/bin/env python

# imports
import logging
from hardware_controller import *
from time import sleep, time
import Queue


class Robot:
    """ Main class for controlling our robot morTimmy

    The brain of the robot is a raspberry Pi and the low level
    electronic are handled by an Arduino. The Arduino provides
    an interface to the DC motors and various sensors
    """

    LOG_FILENAME = 'my_morTimmy.log'
    SENSOR_READ_INTERVAL = 0.5

    arduino = HardwareController()
    runningTime = 0
    lastSensorReading = 0
    isRunning = False
    isStopped = True

    def __init__(self):
        """ Called when the robot class is created.

        It intializes the sensor data queue and sets up the 
        logging output file

        Returns:

        Raises:
          TODO: Add proper error handling.
        """

        logging.basicConfig(filename=self.LOG_FILENAME,
                            level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(message)s')
        logging.info('initialising morTimmy the robot')
        self.sensorDataQueue = Queue.Queue()
        self.initialize()

    def initialize(self):
        """ (re)initializes the robot.

        Responsible for setting up the connection to the Arduino.
        The function loops until a connection is established
        """
        self.arduino.initialize()
        while not self.arduino.isConnected:
            print ("Failed to establish connection to Arduino, retrying in 5s")
            logging.debug('Failed to establish connection to Arduino, retrying in 5s')
            sleep(5)                # wait 5sec before trying again
            self.arduino.initialize()
        logging.info('Connected to Arduino through serial connection') 

    def run(self):
        """ The main robot loop """

        currentTime = time()

        # Check connection to arduino, reinitialize if not
        if not self.arduino.isConnected:
            self.arduino.initialize()

        # If the sensor update time has exceeded
        # update the sensor data
        if (currentTime - self.lastSensorReading) >= self.SENSOR_READ_INTERVAL:
            print "Updated distance sensor, last reading was at %d" % self.lastSensorReading
            logging.info('Updated distance sensor, last reading was at %d' % self.lastSensorReading)
            while not self.sensorDataQueue.empty():
                lastSensorReading = self.sensorDataQueue.get_nowait()
                self.distanceSensorValue = self.arduino.distanceSensorValue
            self.lastSensorReading = currentTime

        # Move robot forward if stopped for 5sec
        if self.isStopped and (self.runningTime - currentTime) >= 5:
            self.arduino.sendMessage(MODULE_MOTOR, CMD_MOTOR_FORWARD, 255)
            self.runningTime = currentTime
            self.isRunning = True
        # Stop robot if running for 5sec
        elif self.isRunning and (self.runningTime - currentTime) >= 5:
            self.arduino.sendMessage(MODULE_MOTOR, CMD_MOTOR_STOP)
            self.runningTime = currentTime
            self.isStopped = True

        # Read bytes from the Arduino and add messages to the Queue if found
        self.arduino.recvMessage()

        # Process all received messages in the queue
        while not self.arduino.recvMessageQueue.empty():
            recvMessage = self.arduino.recvMessageQueue.get_nowait()

            if recvMessage == None:
                # Why does the queue always return a None object?
                break;
            elif recvMessage == 'Invalid':
                logging.error('Received invalid packet, ignoring');
            elif recvMessage['module'] == chr(MODULE_DISTANCE_SENSOR):
                self.sensorDataQueue.put({'sensor': recvMessage['module'],
                                          'data': recvMessage['data']})
            else:
                
                logging.debug("Message with unknown module or command received. Message details:")
                logging.debug("msgID: %d ackID: %d module: %s "
                              "commandType: %s data: %d checksum: %s" % (recvMessage['messageID'],
                                                                          recvMessage['acknowledgeID'],
                                                                          hex(recvMessage['module']),
                                                                          hex(recvMessage['commandType']),
                                                                          recvMessage['data'],
                                                                          hex(recvMessage['checksum'])))


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
