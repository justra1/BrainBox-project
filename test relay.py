import RPi.GPIO as GPIO
import time

# --- การตั้งค่า ---
RELAY_PIN = 17  # ใส่เลข GPIO ที่คุณต่อสาย IN ของ Relay (เช่น GPIO 17)

# เตรียมการทำงาน GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

print(f"Starting Relay Test on GPIO {RELAY_PIN}")
print("Press Ctrl+C to stop...")

try:
    while True:
        # สั่งเปิด
        print("🟢 Relay ON (NO)")
        GPIO.output(RELAY_PIN, GPIO.HIGH)
        time.sleep(2)  # รอ 2 วินาที

        # สั่งปิด
        print("🔴 Relay OFF (NC)")
        GPIO.output(RELAY_PIN, GPIO.LOW)
        time.sleep(2)  # รอ 2 วินาที

except KeyboardInterrupt:
    print("\nStopping test...")

finally:
    GPIO.output(RELAY_PIN, GPIO.LOW) # ปิด Relay ก่อนออก
    GPIO.cleanup() # คืนค่าขา GPIO
    print("GPIO Cleaned up.")
