#!/usr/bin/env python

from hardware_control import HardwareController
import serial


class ArduinoSerialController(HardwareController):

    """ Serial interface into the Arduino microcontroller """

    commands = {'goForward': 'W',
                'goBack': 'S',
                'goLeft': 'A',
                'goRight': 'D'}

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

    def send(self, data):
        """ Send data onto the serial port towards the arduino.

        Used by the generic HardwareController class to send
        commands.

        Args:
          data (str): The data string to send to the arduino. This
            is used by the public sendCommand() function
        """
        print "morTimmy: %s" % data
        self.channel.write(data)

    def recv(self):
        """ Receive data from the Arduino through the serial port.

        Used by the generic HardwareController class to receive
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
        hwControl = ArduinoSerialController()
    except Exception as e:
        print ("Error, could not establish connection to "
               "Arduino through the serial port.\n%s") % e
        exit()
    hwControl.sendCommand('FWD', '255')
    hwControl.sendCommand('STOP')
    hwControl.sendCommand('COMMAND TO LONG!')


if __name__ == '__main__':
    main()
