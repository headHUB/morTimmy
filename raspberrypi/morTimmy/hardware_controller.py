#!/usr/bin/env python

import serial			# pyserial library for serial communications
from struct import *		# Python struct library for constructing the command data

# Definitions

FRAME_FLAG = 0x0C       # Marks the beginning and end of a frame
FRAME_ESC = 0x1B        # Escapes chars in a frame that have a special meaning

CMD_START = 0x00
CMD_START_ACK = 0x00
CMD_STOP = 0x00
CMD_STOP_ACK = 0x00
CMD_RESTART = 0x00
CMD_RESTART_ACK = 0x00

# Motor module specific definitions
CMD_FORWARD = 0x00
CMD_BACK = 0x00
CMD_LEFT = 0x00
CMD_RIGHT = 0x00


class HardwareController():

    """ Serial interface into the Arduino microcontroller

    We use a protocol similar to the PPP protocol used in for
    example ADSL connections. For each message sent over the
    serial connection we will add a FRAME_FLAG to the beginning
    and end. If by change the message itself contains the FRAME_FLAG
    or other special characters we precede the byte with an
    escape flag (FRAME_ESC).

    Since data can be lost in transmission due to hardware errors
    or electrical interference we perform a CRC check on the raw
    message and append that after the message.

     Frame layout
    +------------+---------+-----+------------+
    | FRAME_FLAG | MESSAGE | CRC | FRAME_FLAG |
    +------------+---------+-----+------------+

    Our message consists of the following fields:

    messageID      (unsigned long, 4 bytes, numeric id of the message)
    destination    (unsigned int, 1 byte, arduino module to target)
    commandType    (unsigned int, 1 byte, Type of command to send)
    dataLen        (unsigned int, 1 byte, lenght of message data in Bytes)
    data           (string, dataLen byte(s), the data payload)

    The following generic commands are available currently:
        START, START_ACK:       Starts the specified module.
                                replies ACK with messageID in data field
                                when started
        RESTART, RESTART_ACK    Restarts the specified module,
                                replies ACK with messageID ind data field
                                when restarted
        STOP, STOP_ACK          Stops the specified module, replies
                                with STOP_ACK with messageID in data field
                                when stopped
        REQ_DATA, DATA          Requests data from the specified module,
                                replies with the requested data.

    The following modules are available currently:
        Motors                  Controls the robots motors
        DistanceSensor          Handles the distance sensor
        AccelerationSensor      Handles the Acceleration sensor
        CompassSensor           Handles the Compass sensor
    """

    __lastMessageID = 0         # holds the last used messageID

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
        self.serialPort = serial.Serial(serialPort, baudrate)

    def __del__(self):
        """ Close the serial connection when the class is deleted """
        self.serialPort.close()

    def __packMessage(self, module, commandType, data):
        """ Creates a message understood by the Arduino

          Message structure
        +-----------+--------+-------------+---------+------+----------+
        | MessageID | Module | CommandType | dataLen | Data | Checksum |
        +-----------+--------+-------------+---------+------+----------+

        Args:
            Module   (unsigned int, 1 byte, arduino module to target)
            commandType    (unsigned int, 1 byte, Type of command to send)
            data           (string, dataLen byte(s), the data payload)

        Returns:
            Message byte string

        TODO:
            Need to do validation checks for all given arguments
            Implement CRC checksum on raspberry and arduino
        """

        self.__lastMessageID += 1
        rawMessage = self.__lastMessageID
        rawMessage.append(module)
        rawMessage.append(commandType)
        rawMessage.append(len(data))
        rawMessage.append(data)
        rawMessage.append(data)

        checksum = 'TODO'              # Need to implement CRC checksum
        rawMessage.append(checksum)

        return rawMessage

    def __unpackMessage(self, message):
        pass

    def __packFrame(self, message):
        """ Packs the command into a frame

        Performs checksum calculation, escapes any potential
        characters that matches a frame control flag and applies
        the frame marker to the beginning and end of the frame

        Args:
            message (struct message): The message to be sent to
                                      the arduino

        Returns:
            A packed frame suitable for sending to the arduino
            over the serial connection. """

    def __unpackFrame(self, frame):
        """ Unpacks a received frame from the arduino

        Args:
            frame (string): The received frame from
                            the arduino
        Returns:
            message (struct message): A received message from the
                                      arduino
        """

    def sendMessage(self, module, commandType, data):
        """ Send data onto the serial port towards the arduino.

        Used by the HardwareController class to send commands.

        Args:
          data (str): The data string to send to the arduino. This
            is used by the public sendCommand() function
        """
        print "morTimmy: %s %s" % (command, data)
        self.serialPort.write(' '.join([command, data]))

    def recvMessage(self):
        """ Receive data from the Arduino through the serial port.

        Used by the HardwareController class to receive
        commands from the Arduino.

        Returns:
          returns a single frame received through the serial controller.
        """
        data = self.serialPort.readline()
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
