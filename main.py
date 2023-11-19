#!/usr/bin/env pybricks-micropython

# Initialize the EV3 Brick.
ev3 = EV3Brick()
ev3.speaker.set_volume(100)

# Initialize the motors.
leftMotor = Motor(Port.B)
rightMotor = Motor(Port.C)
grabber= Motor(Port.A)
touch_sensor = TouchSensor(Port.S1)


while True:
    print(touch_sensor.pressed())
    if not touch_sensor.pressed():
        grabber.run(1000)
    else:
        grabber.stop(Stop.HOLD)
        grabber.run_until_stalled(-1000,Stop.HOLD)
        break


# Initialize the drive base.
robotDriveBase = DriveBase(leftMotor, rightMotor, wheel_diameter=25.5, axle_track=145)


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
