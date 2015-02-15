/**
 * @file morTimmy.ino
 * @brief Main program logic for morTimmy the Robot
 * @author Mathijs Mortimer
 */

// INCLUDES

#include "Arduino.h"            // required for access to the core arduino stuff like analogWrite and pinMode
#include "L298N_motor_driver.h"
#include <NewPing.h>
#include "newping_distance_sensor.h"
#include <Servo.h>
#include "raspberry_remote_control.h"

// PIN DEFINITIONS

// DC Motor Pins
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

// Servo Motor Pins
#define BOTTOM_PANTILT_SERVO_PIN 3            // PWM
#define TOP_PANTILT_SERVO_PIN 4               // PWM

// Distance Sensor Pins
#define DISTANCE_SENSOR_TRIG_PIN 22
#define DISTANCE_SENSOR_ECHO_PIN 23
#define TOO_CLOSE 10                         // distance in cm to an obstacle the robot should avoid 
#define MAX_DISTANCE (TOO_CLOSE * 20)        // maximum distance in cm the sensor will measure 

// CLASS DEFINITIONS

namespace morTimmy {
    class Robot {
        public:
            /*
             * @brief Class constructor
             */
            Robot() 
                : leftMotors(FRONT_LEFT_MOTOR_DIRECTION_PIN_1, 
                             FRONT_LEFT_MOTOR_DIRECTION_PIN_2,
                             FRONT_LEFT_MOTOR_SPEED_PIN,
                             REAR_LEFT_MOTOR_DIRECTION_PIN_1,
                             REAR_LEFT_MOTOR_DIRECTION_PIN_2,
                             REAR_LEFT_MOTOR_SPEED_PIN),
                  rightMotors(FRONT_RIGHT_MOTOR_DIRECTION_PIN_1,
                              FRONT_RIGHT_MOTOR_DIRECTION_PIN_2,
                              FRONT_RIGHT_MOTOR_SPEED_PIN,
                              REAR_RIGHT_MOTOR_DIRECTION_PIN_1,
                              REAR_RIGHT_MOTOR_DIRECTION_PIN_2,
                              REAR_RIGHT_MOTOR_SPEED_PIN),
                  distanceSensor(DISTANCE_SENSOR_TRIG_PIN,
                                 DISTANCE_SENSOR_ECHO_PIN,
                                 MAX_DISTANCE)          
            {
            }


            /*
             * @brief initialize the robot
             */
            void initialize()
            {
                Serial.println("Initializing robot");
                leftMotors.setSpeed(255);
                rightMotors.setSpeed(255);
                state = stateRunning;
            }


            /*
             * @brief Update the state of the robot based on input from sensor and/or remote control.
             * Must be called repeatedly while the robot is in operation.
             */
            void run() {
              if (state == stateRunning) {
                if (distanceSensor.getDistance() <= TOO_CLOSE) {
                  state = stateStopped;
                  leftMotors.setSpeed(0);
                  rightMotors.setSpeed(0);
                }    
              }
            }

        private:
            Motor leftMotors;    // Controls the front and rear left DC motors
            Motor rightMotors;   // Controls the front and rear right DC motors
            DistanceSensor distanceSensor;
            enum state_t { stateStopped, stateRunning };    // Various robot states
            state_t state;                                  // Holds the current robot state
            unsigned long stateStartTime;                   // Holds the start time of the current state
    };
};

morTimmy::Robot robot;

void setup() {
    Serial.begin(9600);
    robot.initialize();
}

void loop() {
    robot.run();
}
