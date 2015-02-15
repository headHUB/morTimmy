#!/usr/bin/env python


class HardwareController():
    """ High level interface towards the hardware layer

    It will be able to send and receive data from the microcontroller.
    """

    __commandSize = 1      # Size of the recv and send command in Bytes
    __dataSize = 0        # Size of the recv and send data in Bytes

    def sendCommand(self, command, data=''):
        """ Send a command to the hardware controller.

        The command and data size will be predetermined and combined
        into a single string. This string will be sent to the arduino
        for parsing.

        Args:
          command (str): A command can be less than commandSize and will
            add trailing whitespaces to meet the required commandSize.
          data (str): The data is not mandatory. If no data is provided it will
            be padded with whitespaces to meet the required dataSize.
        """

        if len(command) > self.__commandSize:
            print ("Error: command %s is invalid. Size should be %d "
                   "or smaller" % (command, self.__commandSize))
            return
        if len(data) > self.__dataSize:
            print ("Error: data %s is invalid. Size should be %d "
                   "or smaller" % (data, self.__dataSize))
            return

        sendString = ''.join([command.ljust(self.__commandSize, ' '),
                              data.ljust(self.__dataSize, ' ')])
        self.__send(sendString)

    def getCommand(self):
        """ Retrieve data from the hardware controller

        Returns:
          self.__recv (str): Returns a command received from the hardware
            controller
        """
        return self.__recv()

    def __send(self, data):
        print "Sent: %s" % data

    def __recv(self):
        print "Recv: <create child class of HardwareController>"
        return


def main():
    """ This function will only be called when the library is run directly
    Only to be used to do quick tests on the library.
    """

    print "Hello World, this is the generic hardware driver library"

    hwControl = HardwareController()
    hwControl.sendCommand('FD', '255')

if __name__ == '__main__':
    main()
