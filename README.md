# Building a 4WD Robot based on Arduino and Raspberry Pi

The goal of this project is to build a autonomous robot that can be expanded upon easily in software. The idea is to have a varietity of different sensors available from the start and build a nice looking casing around it.

## Goals

- Autonomous driving robot
- Automatic object avoidance
- Facial recognition
- Video streaming
- Audio playback, Robot voice and music
- Voice control

## Hardware details

I've purchased the following initial hardware from the british site http://www.hobbycomponents.com/. It was the only site that I could find in Europe that had alot of the required components and had a lot of positive reviews.

- 1x Ultrasonic Module HC-SR04 Distance Sensor
- 2x L298N Stepper Motor Driver Controller Board
- 1x Hobby Components Arduino Compatible R3 Mega
- 1x V2 Mega Sensor Shield for Arduino
- 1x SG90 Pan & Titl servo bracket
- 2x Towerpro SG90 Micro servo 9g
- 1x 4 Wheeled Robot Smart Car Chassis Kit DC 3v 5v 6v suitable for Arduino
- 1x 20cm Solderless Female to Female DuPont Jumper Breadboard Wires (40-Cable Pack)

## Project progress

This section outlines the current status of my project. 

What have I done so far:
- Setup (this) github repository, first time working with git so bear with me!
- Created skeleton classes for both Arduino (C++) and the Raspberry Pi (Python)
- Starting to use Docstrings to properly document my code. Trying to follow the
  Google Style Python Docstrings guidelines. Also implemented sphinx on my 
  home server to generate documentation from the Docstrings. The documentation
  can be found in the relevant docs/ directories as well as on my personal
  homepage http://morTimmy.mortimer.nl/
- Received the hardware order I've placed with http://www.hobbycomponents.com/

  ![Screenshot of hardware ordered from hobbycomponents.com](http://raw.github.com/thiezn/morTimmy/master/images/hw_order.jpg)


## Credits

- First have to credit my wife for putting up with me and my time consuming hobbies!

- Next I have to really give credit to Miguel Grindberg. He has created a really excellent tutorial on 
  building an Arduino Robot. I especially like his detailed explanation and he uses a proper Object Oriented 
  structure in his project which allows you to easily expand upon the code. Check it out here: 

  http://blog.miguelgrinberg.com/post/building-an-arduino-robot-part-i-hardware-components
