from gpiozero import Robot, Motor
from time import sleep


SPEED = 0.5

class BrailleWheel(Motor):
    def __init__(self,motor_pins: tuple):
        Motor.__init__(self,forward =motor_pins[0], backward= motor_pins[1])
        self.motor = Motor(forward=motor_pins[0],backward=motor_pins[1])

    @property
    def motor(self):
        return self._motor
    
    @motor.setter
    def motor(self, motor):
        self._motor = motor

    def next_letter(self):
        self.motor.forward()
        sleep(SPEED)
        self.motor.stop()

    def previous_letter(self):
        self.motor.backward()
        sleep(SPEED)
        self.motor.stop()


########################main######################

m1 = BrailleWheel((4,24))
m1.next_letter()
