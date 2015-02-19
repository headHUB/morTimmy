/**
  * @file raspberry_controller.h
  * @brief Raspberry Controller definition for the morTimmy robot
  * @author Mathijs Mortimer
  */
 
namespace morTimmy {

  // Definitions
  // Frames
  byte FRAME_FLAG = 0x0C;       // Marks the start and end of a frame
  byte FRAME_ESC = 0x1B;        // Escape char for frame

  // Arduino
  byte MODULE_ARDUINO = 0x30;
  byte CMD_ARDUINO_START = 0x64;
  byte CMD_ARDUINO_START_NACK = 0x65;
  byte CMD_ARDUINO_STOP = 0x66;
  byte CMD_ARDUINO_STOP_NACK = 0x67;
  byte CMD_ARDUINO_RESTART = 0x68;
  byte CMD_ARDUINO_RESTART_NACK = 0x69;

  // Distance Sensor
  byte MODULE_DISTANCE_SENSOR = 0x31;
  byte CMD_DISTANCE_SENSOR_START = 0x64;
  byte CMD_DISTANCE_SENSOR_NACK = 0x65;
  byte CMD_DISTANCE_SENSOR_STOP = 0x66;
  byte CMD_DISTANCE_SENSOR_STOP_NACK = 0x67;

  // Motor
  byte MODULE_MOTOR = 0x32;
  byte CMD_MOTOR_FORWARD = 0x64;
  byte CMD_MOTOR_FORWARD_NACK = 0x65;
  byte CMD_MOTOR_BACK = 0x66;
  byte CMD_MOTOR_BACK_NACK = 0x67;
  byte CMD_MOTOR_LEFT = 0x68;
  byte CMD_MOTOR_LEFT_NACK = 0x69;
  byte CMD_MOTOR_RIGHT = 0x6A;
  byte CMD_MOTOR_RIGHT_NACK = 0x6B;
  byte CMD_MOTOR_STOP = 0x6C;
  byte CMD_MOTOR_STOP_NACK = 0x6D;

  struct message_t {
        unsigned long messageID;
        unsigned long acknowledgeID;
        unsigned short module;
        unsigned short commandType;
        unsigned short dataLen;
        unsigned int data;
        unsigned int checksum;
  };   

  class RaspberryController {
    public:

      unsigned long lastMessageID;
      /**
        * @brief Class constructor
        */
      RaspberryController() {
        lastMessageID = 0;
      }
      
      /**
        * @brief send a message over the serial interface
        * @param msg: a message_t structure consisting of the message data
        */
      void sendMessage(message_t &msg)
      {
        // Set the messageID
        lastMessageID++;
        msg.messageID = lastMessageID;
        
        // Copy the message into a byte string
        char byteMsg[sizeof(msg)];
        memcpy(byteMsg, &msg, sizeof(msg));
        
        // Create another instance of the message to iterate through
        // if we find a character we need to escape (like the FRAME_FLAG)
        // we append a FRAME_ESC character before it in the byteMsg
        char tmpByteMsg[sizeof(msg)];
        memcpy(tmpByteMsg, &byteMsg, sizeof(msg));
        
        for (int i = 0; i < sizeof(tmpByteMsg); i++) {
          if (tmpByteMsg[i] == FRAME_FLAG || tmpByteMsg[i] == FRAME_ESC) {
            memmove(byteMsg + i + 1,
                    byteMsg + i,
                    sizeof(byteMsg) - (i + 1));
            byteMsg[i] = FRAME_ESC;
          }
        }
        
        // Print the packet bytes to the serial port including
        // the FRAME_FLAG to the start and end of the message
        Serial.write(FRAME_FLAG);
        Serial.write(byteMsg, sizeof(byteMsg));
        Serial.write(FRAME_FLAG);
      }      
  };
};
