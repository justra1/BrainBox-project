from machine import Pin, PWM

# Motor pins
IN1 = Pin(14, Pin.OUT)
IN2 = Pin(15, Pin.OUT)
ENA = PWM(Pin(13))
ENA.freq(1000)

# Current speed (0–65535)
current_speed = 40000    # default ~60%

def set_speed(level):
    """
    level = 0–9
    converts level to 0–65535 PWM
    """
    global current_speed
    if level == 0:
        current_speed = 0
    else:
        current_speed = int((level / 9) * 65535)

    ENA.duty_u16(current_speed)


def motor_forward():
    IN1.high()
    IN2.low()
    ENA.duty_u16(current_speed)


def motor_backward():
    IN1.low()
    IN2.high()
    ENA.duty_u16(current_speed)


def motor_stop():
    IN1.low()
    IN2.low()
    ENA.duty_u16(0)


print("""
Controls:
0 = STOP
1 = FORWARD
2 = BACKWARD
3–9 = SPEED LEVEL
""")

while True:
    cmd = input().strip()

    # STOP
    if cmd == "0":
        print("STOP")
        motor_stop()

    # FORWARD
    elif cmd == "1":
        print("FORWARD, speed:", current_speed)
        motor_forward()

    # BACKWARD
    elif cmd == "2":
        print("BACKWARD, speed:", current_speed)
        motor_backward()

    # SPEED 3–9
    elif cmd.isdigit() and 3 <= int(cmd) <= 9:
        level = int(cmd)
        set_speed(level)
        print("Speed level", level, "=> PWM =", current_speed)

    else:
        print("Invalid input")
