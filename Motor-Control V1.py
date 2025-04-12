from gpiozero import Motor
from time import sleep

SPEED = 9

class BrailleWheel:
    def __init__(self, motor_pins: tuple):
        self.motor = Motor(forward=motor_pins[0], backward=motor_pins[1])
        self.value = 1

    def next_letter(self):
        self.motor.forward()  
        sleep(SPEED)          
        self.motor.stop()  

    def previous_letter(self):
        self.motor.backward()
        sleep(SPEED)          
        self.motor.stop()     

########################main######################

# Create a BrailleWheel instance with motor pins (4, 24)
m1 = BrailleWheel((16, 17))
m2 = BrailleWheel((18,19))
m1.next_letter()
m2.next_letter()
m1.previous_letter()
m2.previous_letter()

