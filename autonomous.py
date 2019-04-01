# Import the RPi.GPIO package
import RPi.GPIO as GPIO
# Set the numbering mode for te program to the BOARD numbering System
GPIO.setmode(GPIO.BOARD)

# Initialize the pins 17,18,22 and 23 as output pins with the initial state as OFF
GPIO.setup(17, GPIO.OUT, initial=0)
GPIO.setup(18, GPIO.OUT, initial=0)
GPIO.setup(22, GPIO.OUT, initial=0)
GPIO.setup(23, GPIO.OUT, initial=0)

# Initialize a pins object to contain PWM instances for all output pins and their dutycycle values
pins = {
    front_left: {
        pwm: GPIO.PWM(17, 1000),
        dc: 1000
    },
    front_right: {
        pwm: GPIO.PWM(18, 1000),
        dc: 1000
    },
    rear_left: {
        pwm: GPIO.PWM(22, 1000),
        dc: 1000
    },
    rear_right: {
        pwm: GPIO.PWM(23, 1000),
        dc: 1000
    }
}


class MovementController(object):
    def __init__(self):
        print("Reseting Motor")
        self.direction = 0
        self.right, self.left, self.front, self.back = [None] * 4
        self.previousDirection = None
        self.CompleteMotorShutdown()
        print("System Initialized!")

    def CompleteMotorShutdown(self):
        # turn all output pins off, set as LOW or 0
        GPIO.output(17, GPIO.LOW)
        GPIO.output(18, GPIO.LOW)
        GPIO.output(22, GPIO.LOW)
        GPIO.output(23, GPIO.LOW)
        print("Motor shutdown!")

    def StartPWM(self, pin):
        # Start PWM with an initial duty cycle of 100% and set dc to 100.
        pin.pwm.start(100)
        pin.dc = 100

    def StopPWM(self, pin):
        # Stop PWM for the given instance.
        pin.pwm.start()
        pin.dc = 0

    def ChangeSpeed(self, pin, duty_cycle):
        # Gradually change the PWM duty cycle of the PWM instance and dc to the duty_cycle value.
        for dc in range(pin.dc, duty_cycle):
            pin.pwm.ChangeDutyCycle(dc)
            pin.dc = dc

    def Move(self, direction):
        # Forward
        if direction == 1:
            # turn the output pins 22 & 23 off, set as LOW or 0
            GPIO.output(22, GPIO.LOW)
            GPIO.output(23, GPIO.LOW)
            # turn the output pins 17 & 18 on, set as HIGH or 1
            GPIO.output(17, GPIO.HIGH)
            GPIO.output(18, GPIO.HIGH)
        # Backward
        if direction == 2:
            # turn the output pins 17 & 18 off, set as LOW or 0
            GPIO.output(17, GPIO.LOW)
            GPIO.output(18, GPIO.LOW)
            # turn the output pins 22 & 23 on, set as HIGH or 1
            GPIO.output(22, GPIO.HIGH)
            GPIO.output(23, GPIO.HIGH)
        # Right
        if direction == 3:
            # turn the output pins 18 & 23 off, set as LOW or 0
            GPIO.output(18, GPIO.LOW)
            GPIO.output(23, GPIO.LOW)
            # turn the output pins 17 & 22 on, set as HIGH or 1
            GPIO.output(17, GPIO.HIGH)
            GPIO.output(22, GPIO.HIGH)
        # Left
        if direction == 4:
            # turn the output pins 17 & 22 off, set as LOW or 0
            GPIO.output(17, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            # turn the output pins 18 & 23 on, set as HIGH or 1
            GPIO.output(18, GPIO.HIGH)
            GPIO.output(23, GPIO.HIGH)

    def MachineMovement(self, left, right, front, back, previousDirection):
        self.left, self.right, self.front, self.back = [
            left, right, front, back]
        # Move Forward
        if (self.right == "green" and self.left == "red" and self.front == None):
            print("Move Forward")
            if (previousDirection == 0 or previousDirection == 1):
                previousDirection = 1
                self.Move(previousDirection)
            elif (previousDirection == 2):
                previousDirection = 1
                self.Move(previousDirection)
            elif (previousDirection == 3):
                previousDirection = 1
                self.Move(previousDirection)
            else:
                previousDirection = 1
                self.Move(previousDirection)

        # Move Backward
        elif (self.left == "green" and self.right == "red" and self.back == None):
            print("Move Backward")
            if (previousDirection == 0 or previousDirection == 2):
                previousDirection = 2
                self.Move(previousDirection)
            elif (previousDirection == 1):
                previousDirection = 2
                self.Move(previousDirection)
            elif (previousDirection == 3):
                previousDirection = 2
                self.Move(previousDirection)
            else:
                previousDirection = 2
                self.Move(previousDirection)

        # Go Right
        elif (self.right == None and self.left == "red"):
            print("Turn Right")
            if (previousDirection == 0 or previousDirection == 3):
                previousDirection = 3
                self.Move(previousDirection)
            elif (previousDirection == 1):
                previousDirection = 3
                self.Move(previousDirection)
            elif (previousDirection == 2):
                previousDirection = 3
                self.Move(previousDirection)
            else:
                previousDirection = 3
                self.Move(previousDirection)

        # Go Left
        elif (self.right == "green" and self.left == None):
            print("Turn Left")
            if (previousDirection == 0 or previousDirection == 4):
                previousDirection = 4
                self.Move(previousDirection)
            elif (previousDirection == 1):
                previousDirection = 4
                self.Move(previousDirection)
            elif (previousDirection == 2):
                previousDirection = 4
                self.Move(previousDirection)
            else:
                previousDirection = 4
                self.Move(previousDirection)
        else:
            print("Stop")
            previousDirection = 0
            self.CompleteMotorShutdown()
            # cleanup GPIO settings before exiting
            GPIO.cleanup()


if __name__ == "__main__":
    mc = MovementController()
    left = "red"
    right = "green"
    front = None
    back = None
    for prevDir in range(0, 4):
        print("TESTING INPUT: \nleft=red, right=green, front=None, back=None, previousDirection="+str(prevDir))
        print('-------------------------------------------------------------------')
        print("OUTPUT:")
        mc.MachineMovement("red", "green", None, None, prevDir)
        print('-------------------------------------------------------------------\n')
    for prevDir in range(0, 4):
        print("TESTING INPUT: \nleft=green, right=red, front=None, back=None, previousDirection="+str(prevDir))
        print('-------------------------------------------------------------------')
        print("OUTPUT:")
        mc.MachineMovement("green", "red", None, None, prevDir)
        print('-------------------------------------------------------------------\n')
    for prevDir in range(0, 4):
        print("TESTING INPUT: \nleft=red, right=None, front=None, back=None, previousDirection="+str(prevDir))
        print('-------------------------------------------------------------------')
        print("OUTPUT:")
        mc.MachineMovement("red", None, None, None, prevDir)
        print('-------------------------------------------------------------------\n')
    for prevDir in range(0, 4):
        print("TESTING INPUT: \nleft=None, right=green, front=None, back=None, previousDirection="+str(prevDir))
        print('-------------------------------------------------------------------')
        print("OUTPUT:")
        mc.MachineMovement(None, "green", None, None, prevDir)
        print('-------------------------------------------------------------------\n')

    for prevDir in range(0, 4):
        print("TESTING INPUT: \nleft=red, right=green, front=black, back=None, previousDirection="+str(prevDir))
        print('-------------------------------------------------------------------')
        print("OUTPUT:")
        mc.MachineMovement("red", "green", "black", None, prevDir)
        print('-------------------------------------------------------------------\n')
    for prevDir in range(0, 4):
        print("TESTING INPUT: \nleft=green, right=red, front=black, back=None, previousDirection="+str(prevDir))
        print('-------------------------------------------------------------------')
        print("OUTPUT:")
        mc.MachineMovement("green", "red", "black", None, prevDir)
        print('-------------------------------------------------------------------\n')
    for prevDir in range(0, 4):
        print("TESTING INPUT: \nleft=red, right=None, front=black, back=None, previousDirection="+str(prevDir))
        print('-------------------------------------------------------------------')
        print("OUTPUT:")
        mc.MachineMovement("red", None, "black", None, prevDir)
        print('-------------------------------------------------------------------\n')
    for prevDir in range(0, 4):
        print("TESTING INPUT: \nleft=None, right=green, front=black, back=None, previousDirection="+str(prevDir))
        print('-------------------------------------------------------------------')
        print("OUTPUT:")
        mc.MachineMovement(None, "green", "black", None, prevDir)
        print('-------------------------------------------------------------------\n')

    for prevDir in range(0, 4):
        print("TESTING INPUT: \nleft=red, right=green, front=None, back=black, previousDirection="+str(prevDir))
        print('-------------------------------------------------------------------')
        print("OUTPUT:")
        mc.MachineMovement("red", "green", None, "black", prevDir)
        print('-------------------------------------------------------------------\n')
    for prevDir in range(0, 4):
        print("TESTING INPUT: \nleft=green, right=red, front=None, back=black, previousDirection="+str(prevDir))
        print('-------------------------------------------------------------------')
        print("OUTPUT:")
        mc.MachineMovement("green", "red", None, "black", prevDir)
        print('-------------------------------------------------------------------\n')
    for prevDir in range(0, 4):
        print("TESTING INPUT: \nleft=red, right=None, front=None, back=black, previousDirection="+str(prevDir))
        print('-------------------------------------------------------------------')
        print("OUTPUT:")
        mc.MachineMovement("red", None, None, "black", prevDir)
        print('-------------------------------------------------------------------\n')
    for prevDir in range(0, 4):
        print("TESTING INPUT: \nleft=None, right=green, front=None, back=black, previousDirection="+str(prevDir))
        print('-------------------------------------------------------------------')
        print("OUTPUT:")
        mc.MachineMovement(None, "green", None, "black", prevDir)
        print('-------------------------------------------------------------------\n')

    for prevDir in range(0, 4):
        print("TESTING INPUT: \nleft=red, right=green, front=black, back=black, previousDirection="+str(prevDir))
        print('-------------------------------------------------------------------')
        print("OUTPUT:")
        mc.MachineMovement("red", "green", "black", "black", prevDir)
        print('-------------------------------------------------------------------\n')
    for prevDir in range(0, 4):
        print("TESTING INPUT: \nleft=green, right=red, front=black, back=black, previousDirection="+str(prevDir))
        print('-------------------------------------------------------------------')
        print("OUTPUT:")
        mc.MachineMovement("green", "red", "black", "black", prevDir)
        print('-------------------------------------------------------------------\n')
    for prevDir in range(0, 4):
        print("TESTING INPUT: \nleft=red, right=None, front=black, back=black, previousDirection="+str(prevDir))
        print('-------------------------------------------------------------------')
        print("OUTPUT:")
        mc.MachineMovement("red", None, "black", "black", prevDir)
        print('-------------------------------------------------------------------\n')
    for prevDir in range(0, 4):
        print("TESTING INPUT: \nleft=None, right=green, front=black, back=black, previousDirection="+str(prevDir))
        print('-------------------------------------------------------------------')
        print("OUTPUT:")
        mc.MachineMovement(None, "green", "black", "black", prevDir)
        print('-------------------------------------------------------------------\n')


# Author: Pranali Deshmukh
# Date:    24/02/2019
# Updated: 03/02/2019
