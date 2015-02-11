/**
 * @file morTimmy.ino
 * @brief Main program logic for morTimmy the Robot
 * @author Mathijs Mortimer
 */

namespace morTimmy {
    class Robot {
        public:
            /*
             * @brief Class constructor
             */
            Robot() {
                initialize();
            }

            /*
             * @brief initialize the robot
             */
            void initialize()
            {
                Serial.println "Initializing robot";
            }

            void run() {
            }
    };
};

morTimmy::Robot robot;

void setup() {
    Serial.begin(115400);
    robot.initialize();
}

void loop() {
    robot.run();
}
