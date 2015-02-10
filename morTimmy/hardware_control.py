#!/usr/bin/env python


class HardwareController():
    """ This class is an abstraction layer to allow communication
        to the low level hardware layer. It will be able to send
        and receive data from the microcontroller.
    """

    def __init__(self, communicationChannel):
        """ The initialisation for the HardwareController class. It
            requires the ID of the communication channel to the
            microcontroller.
        """

        self.communicationChannel = communicationChannel

    def setCommand(self, module, command):
        """ This function will send a command to the specified module """
        pass

    def getCommand(self, module):
        """ This function will retrieve data from the specified module """
        return


def main():
    """ This function will only be called when the library is run directly
        Only to be used to do quick tests on the library.
    """

    print "Hello World, this is the generic hardware driver library"

if __name__ == '__main__':
    main()
