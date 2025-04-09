from gpiozero import Robot, Motor
from time import sleep

robot = Robot(left=Motor(4, 14), right=Motor(17, 18))

for i in range(4):
    robot.forward()
    sleep(10)
    robot.right()
    sleep(1)

SPEED = 0.5

class BrailleWheel(Robot):
    def __init__(self,motor_pins):
        Robot.__init__(motor=Motor(motor_pins))
        self.motor = Motor(motor_pins)

    @property
    def motor(self):
        return self.motor
    
    @motor.setter
    def motor(self, motor):
        self.motor = motor

    def next_letter(self):
        self.motor.forward()
        sleep(SPEED)
        self.motor.stop()

    def previous_letter(self):
        self.motor.backward()
        sleep(SPEED)
        self.motor.stop()