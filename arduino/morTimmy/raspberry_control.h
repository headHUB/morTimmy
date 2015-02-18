/**
  * @file raspberry_controller.h
  * @brief Raspberry Controller definition for the morTimmy robot
  * @author Mathijs Mortimer
  */
 
namespace morTimmy {
  class RaspberryController {
    public:    
      /**
        * @brief Class constructor
        */
      RaspberryController() {}
      
      
      /**
        * @brief Return the next remote command, if available
        * @param cmd A reference to a command_t struct where the
                     information will be stored
        * @ return true if a remote command is available, false if not
        */
      virtual bool recvCommand() {
      }
  };
};
