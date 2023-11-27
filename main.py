#!/usr/bin/env pybricks-micropython
from robot import Robot

# Initialize the EV3 Brick.
# ev3 = EV3Brick()
# ev3.speaker.set_volume(100)

# # Initialize the motors.
# leftMotor = Motor(Port.B)
# rightMotor = Motor(Port.C)
# grabber= Motor(Port.A)
# touch_sensor = TouchSensor(Port.S1)

robot = Robot()

robot.move(5)
robot.rotate(45)
robot.grab()
robot.release()


# robotDriveBase.settings(1020,250,270,100)
# Go forward and backwards for one meter.
# robotDriveBase.straight(100)
# ev3.speaker.beep()

# robotDriveBase.straight(-100)
# ev3.speaker.beep()

# # Turn clockwise by 360 degrees and back again.
# robotDriveBase.turn(360)
# ev3.speaker.beep()

# robotDriveBase.turn(-360)
# ev3.speaker.beep()

# ev3.speaker.play_file("f1_pit_stop.wav")
# ev3.speaker.say("Do you even lift bro!")
# ev3.speaker.say("Bet you dont even bench 225")
