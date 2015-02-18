#!/usr/bin/env python

import serial			    # pyserial library for serial communications
import struct 	     	# Python struct library for constructing the command data
from zlib import crc32      # used to calculate a message checksum

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

    Since data can be lost or mangled in transmission due to hardware
    errors or electrical interference we perform a CRC check on the
    raw message and append that after the message.

     Frame layout
    +------------+---------+-----+------------+
    | FRAME_FLAG | MESSAGE | CRC | FRAME_FLAG |
    +------------+---------+-----+------------+

    Our message consists of the following fields:

    messageID      (unsigned long, 4 bytes, numeric id of the message)
    destination    (unsigned short, 2 byte, arduino module to target)
    commandType    (unsigned short, 1 byte, Type of command to send)
    dataLen        (unsigned short, 1 byte, lenght of message data in Bytes)
    data           (string, dataLen byte(s), the data payload)
    checksum       (unsigned int, 4 bytes, CRC32)

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
        DATA                    Sends data related to the specified module,
                                an example is a Distance Sensor reporting
                                back its values when STARTed

    The following modules are available currently:
        Motors                  Controls the robots motors
        DistanceSensor          Handles the distance sensor
        AccelerationSensor      Handles the Acceleration sensor
        CompassSensor           Handles the Compass sensor
    """

    __lastMessageID = 0         # holds the last used messageID

    def initialize(self, serialPort='/dev/ttyACM0',
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
        try:
            self.serialPort.close()
        except:
            pass

    def __packMessage(self, module, commandType, data):
        """ Creates a message understood by the Arduino

          Message structure
        +-----------+--------+-------------+---------+------+----------+
        | messageID | module | commandType | dataLen | data | checksum |
        +-----------+--------+-------------+---------+------+----------+

        Args:
            module:      (unsigned int, 1 byte, arduino module to target)
            commandType: (unsigned int, 1 byte, Type of command to send)
            data:        (string, dataLen byte(s), the data payload)

        Returns:
            Message byte string

        TODO:
            Need to do validation checks for all given arguments
            Implement CRC checksum on raspberry and arduino
        """

        self.__lastMessageID += 1

        # pack the message into binary format using ! for platform independency
        # (big-endian, standard type size, no pad bytes). Then calculate
        # the packet checksum and repack the message

        checksum = 0
        rawMessage = struct.pack('!LccHsi',
                                 self.__lastMessageID,
                                 module,
                                 commandType,
                                 len(data),
                                 data,
                                 checksum)

        checksum = crc32(rawMessage[-4])

        rawMessage = struct.pack('!LccHsi',
                                 self.__lastMessageID,
                                 module,
                                 commandType,
                                 len(data),
                                 data,
                                 checksum)

        return rawMessage

    def __unpackMessage(self, message):
        """ Unpacks a message received from the Arduino

        Args:
            message (struct): A message unpacked from a received FRAME_FLAG

        Returns:
            A dict containing:
               messageID
               module
               commandType
               dataLen
               data
        """

        (messageID, module, commandType,
         dataLen, data, recvChecksum) = struct.unpack('!LccHsi', message)

        checksum = 0
        calcChecksum = crc32(struct.pack('!LccHsi',
                                         messageID,
                                         module,
                                         commandType,
                                         dataLen,
                                         data,
                                         checksum)[-4])

        if recvChecksum == calcChecksum:
            return messageID, module, commandType, dataLen, data
        else:
            return None     # invalid packet

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

        frame = b''
        frame += chr(FRAME_FLAG)

        for byte in message:
            if (byte == chr(FRAME_ESC)) or (byte == chr(FRAME_FLAG)):
                frame += chr(FRAME_ESC)
                frame += byte          # TODO, Need to XOR this value?
            else:
                frame += byte

        frame += chr(FRAME_FLAG)

        return frame

    def __unpackFrame(self, frame):
        """ Unpacks a received frame from the arduino

        Args:
            frame (string): The received frame from
                            the arduino
        Returns:
            message (struct message): A received message from the
                                      arduino
        """

        nextByteValid = False
        message = b''

        if(frame[:1] != chr(FRAME_FLAG)) or (frame[-1:] != chr(FRAME_FLAG)):
            print "Invalid frame received, frame flag not valid"
        else:
            for byte in frame:
                if nextByteValid:
                    message += byte
                    nextByteValid = False
                elif (byte == chr(FRAME_ESC)):
                        nextByteValid = True
                elif (byte != chr(FRAME_FLAG)):
                        message += byte

        return message

    def sendMessage(self, module, commandType, data):
        """ Send data onto the serial port towards the arduino.

        Used by the HardwareController class to send commands.

        Args:
          data (str): The data string to send to the arduino. This
            is used by the public sendCommand() function
        """

        print "morTimmy: %s %s %s" % (module, commandType, data)
        self.serialPort.write(' '.join([module, commandType, data]))

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

    def testMessagePacking(self, module, commandType, data):
        """ Test for the message pack and unpack functions """

        print "Packing message..."
        packedMessage = self.__packMessage(module, commandType, data)
        print ''.join(["\\x%02x" % ord(x) for x in packedMessage])

        print "Packing message into frame..."
        frame = self.__packFrame(packedMessage)
        print ''.join(["\\x%02x" % ord(x) for x in frame])

        print "Unpacking message from frame..."
        unpackedFrame = self.__unpackFrame(frame)
        print ''.join(["\\x%02x" % ord(x) for x in unpackedFrame])

        print "Unpacking message..."
        unpackedMessage = self.__unpackMessage(packedMessage)
        print unpackedMessage



def main():
    """ This function will only be called when the library is
    run directly. Only to be used to do quick tests on the library.
    """

    try:
        hwControl = HardwareController()
    except Exception as e:
        print ("Error, could not establish connection to "
               "Arduino through the serial port.\n%s") % e
#        exit()

    hwControl.testMessagePacking('a', 'b', 'c')


if __name__ == '__main__':
    main()
