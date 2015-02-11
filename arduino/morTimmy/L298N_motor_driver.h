/**
 * @file L298N_motor_driver.h
 * @brief Motor device driver for the L298N motor driver controller
 * @author Mathijs Mortimer
 */

#include "motor_driver.h"

namespace morTimmy {
    class Motor : public MotorDriver {
        public:
            /*
             * @brief Class constructor.
             * @param motorXDir1, motorXDir2: controls the motor direction
             * @param motorXspeed: constrols the motor speed, has to be a PWM pin
             */
            Motor(int motorADir1, motorADir2, motorASpeed, motorBDir1, motorBDir2, motorBSpeed) : MotorDriver(), motor(number), currentSpeed(0) {
                // define the L298N Dual H-Bridge Motor Controller Pins
                pinMode(motorAdir1, OUTPUT)
                pinMode(motorAdir2, OUTPUT)
                pinMode(motorAspeed, OUTPUT)
                pinMode(motorBdir1, OUTPUT)
                pinMode(motorBdir2, OUTPUT)
                pinMode(motorBspeed, OUTPUT)
            }

            void setSpeed(int speed) {
                currentSpeed = speed;
                if (speed >= 0) {
                    // Motor A
                    analogWrite(motorAspeed, speed)     // Set speed through PWM
                    digitalWrite(motorADir1, LOW);      // Move motor forward/stop
                    digitalWrite(motorADir2, HIGH);     // Move motor forward/stop
                    // Motor B
                    analogWrite(motorBspeed, speed)     // Set speed through PWM
                    digitalWrite(motorBDir1, LOW);      // Move motor forward/stop
                    digitalWrite(motorBDir2, HIGH);     // Move motor forward/stop
                }
                else {
                    // Motor A
                    analogWrite(motorAspeed, -speed);       // Set negative speed through PWM
                    digitalWrite(motorADir1, HIGH);         // Move motor backwards 
                    digitalWrite(motorADir2, LOW);          // Move motor backwards
                    // Motor B
                    motor.setSpeed(motorAspeed, -speed);    // Set negative speed through PWM
                    digitalWrite(motorADir1, HIGH);         // Move motor backwards
                    digitalWrite(motorADir2, LOW);          // Move motor backwards
                }
            }

            int getSpeed() const {
                return currentSpeed
            }

        private:
            int currentSpeed;
    };
};
