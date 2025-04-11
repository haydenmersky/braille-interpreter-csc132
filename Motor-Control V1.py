from gpiozero import Motor
from time import sleep

SPEED = 0.5

class BrailleWheel:
    def __init__(self, motor_pins: tuple):
        # Initialize the Motor object directly
        self.motor = Motor(forward=motor_pins[0], backward=motor_pins[1])

    def next_letter(self):
        self.motor.forward()  # Move forward
        sleep(SPEED)          # Wait for the desired duration
        self.motor.stop()     # Stop the motor

    def previous_letter(self):
        self.motor.backward() # Move backward
        sleep(SPEED)          # Wait for the desired duration
        self.motor.stop()     # Stop the motor

########################main######################

# Create a BrailleWheel instance with motor pins (4, 24)
m1 = BrailleWheel((4, 24))
m1.next_letter()  # Call the next_letter method
