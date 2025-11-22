import RPi.GPIO as GPIO
import time

# GPIO pins
IN1 = 17
IN2 = 27
ENA = 22   # PWM pin

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

pwm = GPIO.PWM(ENA, 1000)   # PWM at 1 kHz
pwm.start(0)                # start with 0% duty cycle

current_speed = 60          # default speed (percent)

def set_speed(level):
    global current_speed
    current_speed = int((level / 9) * 100)  # convert 0–9 to 0–100%
    pwm.ChangeDutyCycle(current_speed)

def motor_forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(current_speed)

def motor_backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    pwm.ChangeDutyCycle(current_speed)

def motor_stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(0)

print("""
Controls:
0 = STOP
1 = FORWARD
2 = BACKWARD
3–9 = SPEED CONTROL
""")

try:
    while True:
        cmd = input().strip()

        if cmd == "0":
            print("STOP")
            motor_stop()

        elif cmd == "1":
            print("FORWARD at", current_speed, "%")
            motor_forward()

        elif cmd == "2":
            print("BACKWARD at", current_speed, "%")
            motor_backward()

        elif cmd.isdigit() and 3 <= int(cmd) <= 9:
            level = int(cmd)
            set_speed(level)
            print("Speed set to level", level, "=>", current_speed, "%")

        else:
            print("Invalid command")

except KeyboardInterrupt:
    pass

finally:
    pwm.stop()
    GPIO.cleanup()
