#!/usr/bin/env python

import serial			# pyserial library for serial communications
from struct import *		# Python struct library for constructing the command data

# Definitions
FRAME_FLAG 0x0C 	# Used to mark the beginning and end of a frame 
FRAME_ESC 0x1B		# Used to mark the next byte as part of the data 
			# instead of a control flag (e.g. FRAME_FLAG or FRAME_ESC)


class HardwareController():

    """ Serial interface into the Arduino microcontroller """

    def __init__(self, serialPort='/dev/ttyACM0',
                 baudrate=9600,
                 stopbits=serial.STOPBITS_ONE,
                 bytesize=serial.EIGHTBITS,
                 timeout=0):
        """ The initialisation for the ArduinoSerialController class

        Args:
          serialPort (str): The port used to communicate with the Arduino
          baudrate (int): The baudrate of the serial connection
          stopbits (int): The stopbits of the serial connection
          bytesize (int): The bytesize of the serial connection
          timeout (float): The timeout for the serial read command
                           None wait forever
                           0 non blocking
                           x set timeout to x seconds (float allowed)
        """
        self.channel = serial.Serial(serialPort, baudrate)

    def __del__(self):
        """ Close the serial connection when the class is deleted """
        self.channel.close()

    def sendCommand(self, command, data=''):
        """ Send data onto the serial port towards the arduino.

        Used by the HardwareController class to send commands.

        Args:
          data (str): The data string to send to the arduino. This
            is used by the public sendCommand() function
        """
        print "morTimmy: %s %s" % (command, data)
        self.channel.write(' '.join([command, data]))

    def recvCommand(self):
        """ Receive data from the Arduino through the serial port.

        Used by the HardwareController class to receive
        commands from the Arduino.

        Returns:
          returns the data received through the serial controller.
          It will only grab the amount of bytes that consists of a
          command and it's corresponding data
        """
        data = self.channel.readline()
        if data:
            return data.strip()
        else:
            return None


def main():
    """ This function will only be called when the library is
    run directly. Only to be used to do quick tests on the library.
    """

    try:
        hwControl = HardwareController()
    except Exception as e:
        print ("Error, could not establish connection to "
               "Arduino through the serial port.\n%s") % e
        exit()
    hwControl.sendCommand('FWD', '255')
    hwControl.sendCommand('STOP')
    hwControl.sendCommand('COMMAND TO LONG!')


if __name__ == '__main__':
    main()
