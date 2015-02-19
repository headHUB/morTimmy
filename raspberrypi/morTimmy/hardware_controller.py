#!/usr/bin/env python

import serial			    # pyserial library for serial communications
import struct 	         	# Python struct library for constructing the message
import Queue
from zlib import crc32      # used to calculate a message checksum
from time import sleep


# Definitions

# Frames
FRAME_FLAG = 0x0C       # Marks the start and end of a frame
FRAME_ESC = 0x1B        # Escape char for frame

# Arduino
MODULE_ARDUINO = 0x30
CMD_ARDUINO_START = 0x64
CMD_ARDUINO_START_NACK = 0x65
CMD_ARDUINO_STOP = 0x66
CMD_ARDUINO_STOP_NACK = 0x67
CMD_ARDUINO_RESTART = 0x68
CMD_ARDUINO_RESTART_NACK = 0x69

# Distance Sensor
MODULE_DISTANCE_SENSOR = 0x31
CMD_DISTANCE_SENSOR_START = 0x64
CMD_DISTANCE_SENSOR_NACK = 0x65
CMD_DISTANCE_SENSOR_STOP = 0x66
CMD_DISTANCE_SENSOR_STOP_NACK = 0x67

# Motor
MODULE_MOTOR = 0x32
CMD_MOTOR_FORWARD = 0x64
CMD_MOTOR_FORWARD_NACK = 0x65
CMD_MOTOR_BACK = 0x66
CMD_MOTOR_BACK_NACK = 0x67
CMD_MOTOR_LEFT = 0x68
CMD_MOTOR_LEFT_NACK = 0x69
CMD_MOTOR_RIGHT = 0x6A
CMD_MOTOR_RIGHT_NACK = 0x6B
CMD_MOTOR_STOP = 0x6C
CMD_MOTOR_STOP_NACK = 0x6D


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
    acknowledgeID  (unsigned long, 4 bytes, numeric id of the messageID
                    it replied to)
    module         (unsigned short, 2 byte, arduino module to target)
    commandType    (unsigned short, 1 byte, Type of command to send)
    dataLen        (unsigned short, 1 byte, lenght of message data in Bytes)
    data           (string, dataLen byte(s), the data payload)
    checksum       (unsigned int, 4 bytes, CRC32)

    The commandType depicts the action that has to take place on the
    specified module. If the action is succesful the other party will
    reply with the same module and commandType. In addition it will
    put the messageID of the original request in the acknowledgeID field.
    If the command failed to run a NACK messaage will be send with the
    acknowledgeID field filled in.

    The data field contains data that might be returned like the distance
    from a distance sensor.

    The following modules are available currently:
        Arduino                 Controls the Arduino itself
        Motor                   Controls the robots motors
        Servo                   Controls the Servo motors
        DistanceSensor          Handles the distance sensor
        AccelerationSensor      Handles the Acceleration sensor
        CompassSensor           Handles the Compass sensor
    """

    __lastMessageID = 0         # holds the last used messageID
    isConnected = False

    def __init__(self):
        """ Initializes the HardwareController

        TODO: Implement threading/queuing for the serial
        read process
        """

        self.recvMessageQueue = Queue.Queue()

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

        try:
            print ("Opening serial connection to arduino on"
                   "port %s with baudrate %d") % (serialPort, baudrate)
            self.serialPort = serial.Serial(serialPort, baudrate)
            print "Connected to Arduino"

            '''  Reset the arduino by setting the DTR pin LOW and then
            HIGH again. This is the same as pressing the reset button
            on the Arduino itself. The flushInput() whilst the reset
            is in progress is to ensure there is no data from before
            the Arduino was reset in the serial buffer '''

            print "Resetting Arduino using DTR pin"
            self.serialPort.setDTR(level=False)
            sleep(0.5)
            self.serialPort.flushInput()
            self.serialPort.setDTR()
            sleep(0.5)

            print ("TODO: implement proper handshake between Arduino "
                   "and Pi to make sure it's initalised properly")

            ''' TODO implement a handshake between the arduino and Pi
            make sure we're not doing anything until the handshake is
            finalised. '''

            self.serialPort.timeout = 0.1     # Set blocking read to 5 sec
            handshake = self.serialPort.readline()
            print "Recv from Arduino: %s" % handshake
            self.serialPort.timeout = 0     # set non-blocking read
            self.isConnected = True
        except OSError:
            print "Failed to connect to Arduino on serial port %s" % serialPort
            self.isConnected = False
        except Exception, e:
            print "Unexpected error whilst connecting to Arduino"
            print "Exception: %s Error: %s" % (Exception, e)
            self.isConnected = False

    def __del__(self):
        """ Close the serial connection when the class is deleted """
        try:
            self.serialPort.close()
        except:
            pass

    def __packMessage(self, module, commandType, data='', acknowledgeID=0):
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
        rawMessage = struct.pack('!LLccHsi',
                                 self.__lastMessageID,
                                 acknowledgeID,
                                 chr(module),
                                 chr(commandType),
                                 len(data),
                                 data,
                                 checksum)

        checksum = crc32(rawMessage[-4])

        rawMessage = struct.pack('!LLccHsi',
                                 self.__lastMessageID,
                                 acknowledgeID,
                                 chr(module),
                                 chr(commandType),
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

        (messageID, acknowledgeID, module, commandType,
         dataLen, data, recvChecksum) = struct.unpack('!LLccHsi', message)

        checksum = 0
        calcChecksum = crc32(struct.pack('!LLccHsi',
                                         messageID,
                                         acknowledgeID,
                                         module,
                                         commandType,
                                         dataLen,
                                         data,
                                         checksum)[-4])

        if recvChecksum == calcChecksum:
            return ({'messageID': messageID,
                     'acknowledgeID': acknowledgeID,
                     'module': ord(module),
                     'commandType': ord(commandType),
                     'dataLen': dataLen,
                     'data': data})
        else:
            self.responseQueue.put("Invalid")
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
            self.recvMessageQueue.put("Invalid")
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

    def sendMessage(self, module, commandType, data, acknowledgeID=0):
        """ Send data onto the serial port towards the arduino.

        Used by the HardwareController class to send commands.

        Args:
          data (str): The data string to send to the arduino. This
            is used by the public sendCommand() function
        """

        if not self.isConnected:
            print "sendMessage: Not connected to Arduino"
            return None

        packedMessage = self.__packMessage(module,
                                           commandType,
                                           data,
                                           acknowledgeID)
        packedFrame = self.__packFrame(packedMessage)

        print ("morTimmy: "
               "msgID=%d "
               "ackID=%d "
               "module=%s "
               "cmd=%s "
               "dataLen=%d "
               "data=%s ") % (self.__lastMessageID, acknowledgeID, hex(module),
                              hex(commandType), len(data), data)
        # self.serialPort.write(packedFrame)

    def recvMessage(self):
        """ Receive data from the Arduino through the serial port.

        Used by the HardwareController class to receive
        commands from the Arduino.

        Returns:
            (messageID, acknowledgeID, module, commandType, dataLen, data)
        """

        if not self.isConnected:
            print "recvMessage: Not connected to Arduino"
            return None

        message = b''
        foundStartOfFrame = False
        foundEndOfFrame = False
        foundEscFlag = False

        self.serialPort.timeout = 5
        message = self.serialPort.readline()
        if message is not None and message is not '':
            print "TEMP READLINE UNTIL SERIAL PROTO IS CODED ON ARDUINO"
            print "%s" % message
            self.recvMessageQueue.put(message)

        '''
        while not foundEndOfFrame:
            recvByte = self.serialPort.read(1)
            if recvByte == FRAME_FLAG and not foundStartOfFrame:
                # Beginning of our message
                foundStartOfFrame = True
                message += recvByte
            elif (foundStartOfFrame) and \
                 (recvByte == FRAME_ESC) and not foundEscFlag:
                # Found an escape flag which was not escaped itself
                foundEscFlag = True
            elif foundStartOfFrame and foundEscFlag:
                # Byte preceded by FLAG_ESC so treat as normal data
                foundEscFlag = False
                message += recvByte
            elif foundStartOfFrame and not foundEscFlag:
                # regular data part of message
                message += recvByte
            elif foundStartOfFrame and recvByte == FRAME_FLAG:
                # Found ending FRAME_FLAG
                foundEndOfFrame = True
                message += recvByte

        unpackedFrame = self.__unpackFrame(message)
        unpackedMessage = self.__unpackMessage(unpackedFrame)

        print "Arduino: %s" % unpackedMessage
        self.recvMessageQueue.put(unpackedMessage)
        '''

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
        arduino = HardwareController()
    except Exception as e:
        print ("Error, could not establish connection to "
               "Arduino through the serial port.\n%s") % e
#        exit()

    arduino.initialize()
    arduino.sendMessage(MODULE_MOTOR, CMD_MOTOR_FORWARD, 'c')
    arduino.recvMessage()


if __name__ == '__main__':
    main()
