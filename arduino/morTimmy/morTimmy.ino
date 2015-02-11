/**
 * @file morTimmy.ino
 * @brief Main program logic for morTimmy the Robot
 * @author Mathijs Mortimer
 */

// INCLUDES

#include "L298N_motor_driver.h"


// PIN DEFINITIONS

// Motor Pins
#define FRONT_LEFT_MOTOR_DIRECTION_PIN_1 1
#define FRONT_LEFT_MOTOR_DIRECTION_PIN_2 2
#define FRONT_LEFT_MOTOR_SPEED_PIN 3          // Has to be a PWM supported pin

#define REAR_LEFT_MOTOR_DIRECTION_PIN_1 4
#define REAR_LEFT_MOTOR_DIRECTION_PIN_2 5
#define REAR_LEFT_MOTOR_SPEED_PIN 6           // Has to be a PWM supported pin

#define FRONT_RIGHT_MOTOR_DIRECTION_PIN_1 7
#define FRONT_RIGHT_MOTOR_DIRECTION_PIN_2 8
#define FRONT_RIGHT_MOTOR_SPEED_PIN 9         // Has to be a PWM supported pin

#define REAR_RIGHT_MOTOR_DIRECTION_PIN_1 10
#define REAR_RIGHT_MOTOR_DIRECTION_PIN_2 11
#define REAR_RIGHT_MOTOR_SPEED_PIN 12         // Has to be a PWM supported pin

// Distance Sensor Pins


// CLASS DEFINITIONS

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
                state = stateStopped;
                stateStartTime = millis();
            }


            /*
             * @brief Update the state of the robot based on input from sensor and/or remote control.
             * Must be called repeatedly while the robot is in operation.
             */
            void run() {
                unsigned long currentTime = millis();
                unsigned long elapsedTime = currentTime - stateStartTime;
                switch(state) {
                    case stateStopped:
                        if (elapsedTime >= 5000) {
                            leftMotors.setSpeed(255);
                            rightMotors.setSpeed(255);
                            state = stateRunning;
                            stateStartTime = currentTime;
                        }
                        break;
                    case stateRunning:
                        if (elapsedTime >= 8000) {
                            leftMotors.setSpeed(0);
                            rightMotors.setSpeed(0);
                            state = stateStopped;
                            stateStartTime = currentTime;
                        }
                        break;
                    }
                }

        private:
            // Controls the front and rear left DC motors
            Motor leftMotors(FRONT_LEFT_MOTOR_DIRECTION_PIN_1,
                             FRONT_LEFT_MOTOR_DIRECTION_PIN_2,
                             FRONT_LEFT_MOTOR_SPEED_PIN,
                             REAR_LEFT_MOTOR_DIRECTION_PIN_1,
                             REAR_LEFT_MOTOR_DIRECTION_PIN_2,
                             REAR_LEFT_MOTOR_SPEED_PIN)

            // Controls the front and rear right DC motors
            Motor rightMotors(FRONT_RIGHT_MOTOR_DIRECTION_PIN_1,
                              FRONT_RIGHT_MOTOR_DIRECTION_PIN_2,
                              FRONT_RIGHT_MOTOR_SPEED_PIN,
                              REAR_RIGHT_MOTOR_DIRECTION_PIN_1,
                              REAR_RIGHT_MOTOR_DIRECTION_PIN_2,
                              REAR_RIGHT_MOTOR_SPEED_PIN)

            // Private variables related to the robot state
            enum state_t { stateStopped, stateRunning };
            state_t state                                   // Holds the current robot state
            unsigned long stateStartTime;                   // Holds the start time of the current state
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
