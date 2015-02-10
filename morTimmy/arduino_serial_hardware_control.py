#!/usr/bin/env python

from hardware_control import HardwareController
import serial

COMMAND_SIZE = 4        # Size of serial command in bytes
DATA_SIZE = 12          # Size of data in bytes


class ArduinoSerialController(HardwareController):
    """ This class is an abstraction layer to allow communication
        to the low level hardware layer. It will be able to send
        and receive data from the microcontroller.
    """

    def __init__(self, communicationChannel='/dev/tty.usbserial',
                 baudrate=115200,
                 stopbits=serial.STOPBITS_ONE,
                 bytesize=serial.EIGHTBITS):
        """ The initialisation for the ArduinoSerialController class
            It requires the ID of the communication channel to the
            microcontroller.
        """
        try:
            self.channel = serial.Serial(communicationChannel, baudrate)
        except Exception as e:
            self.channel = None
            print ("Error: Could not establish serial connection "
                   "to %s.\n%s" % (communicationChannel, e))

    def sendCommand(self, command, data=''):
        """ This function will send a command to the specified module.
            The command and data size will be predetermined and combined
            into a single string. This string will be sent to the arduino
            for parsing.

            A command can be less than COMMAND_SIZE and will
            add trailing whitespaces to meet the required COMMAND_SIZE.

            The data is not mandatory. If no data is provided it will
            be padded with whitespaces to meet the required DATA_SIZE.
        """

        if len(command) > COMMAND_SIZE:
            print ("Error: command %s is invalid. Size should be %d"
                   "or smaller" % (command, COMMAND_SIZE))
        if len(data) > DATA_SIZE:
            print ("Error: data %s is invalid. Size should be %d"
                   "or smaller" % (data, DATA_SIZE))

        serialCommand = ''.join([command.ljust(COMMAND_SIZE, ' '),
                                data.ljust(DATA_SIZE, ' ')])
        # self.channel.write(serialCommand)
        print serialCommand

    def recvCommand(self, module):
        """ This function will retrieve data from the specified module """
        return


def main():
    """ This function will only be called when the library is run directly
        Only to be used to do quick tests on the library.
    """

    arduinoControl = ArduinoSerialController()
    arduinoControl.sendCommand('FWD', '255')
    arduinoControl.sendCommand('STOP')
    arduinoControl.sendCommand('FAULTY COMMAND')


if __name__ == '__main__':
    main()
