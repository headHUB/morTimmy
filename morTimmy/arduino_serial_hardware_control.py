#!/usr/bin/env python

from hardware_control import HardwareController
import serial


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
            exit()

    def setCommand(self, module, moduleID, command):
        """ This function will send a command to the specified module """

        serialCommand = ':'.join(module, moduleID, command)
        self.channel.write(serialCommand)
        print serialCommand

    def getCommand(self, module):
        """ This function will retrieve data from the specified module """
        return


def main():
    """ This function will only be called when the library is run directly
        Only to be used to do quick tests on the library.
    """

    arduinoControl = ArduinoSerialController()
    arduinoControl.sendCommand('Motor', '1', '255')

if __name__ == '__main__':
    main()
