import asyncio
import RPi.GPIO as GPIO  # เพิ่ม Library สำหรับคุม GPIO
from bleak import BleakClient

# --- การตั้งค่า BLE ---
DEVICE_ADDRESS = "6C:C8:40:58:AE:62"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

# --- การตั้งค่า GPIO (Relay) ---
RELAY_PIN = 17  # เลือกใช้ขา GPIO 17 (Pin 11 บนบอร์ด)

# ตั้งค่าโหมด GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.LOW)  # เริ่มต้นให้เป็น OFF (NC)

async def main():
    print(f"Connecting to {DEVICE_ADDRESS} ...")

    try:
        async with BleakClient(DEVICE_ADDRESS) as client:
            print(f"Connected: {client.is_connected}")
            print("-" * 40)
            print("Commands:")
            print(" - Type 'ON'  : Switch Relay to NO")
            print(" - Type 'OFF' : Switch Relay to NC")
            print(" - Type 1-9   : Send via BLE")
            print(" - Type 'q'   : Quit")
            print("-" * 40)

            while True:
                # 1. รับค่า Input (ใช้ run_in_executor เพื่อไม่ให้บล็อก BLE)
                user_input = await asyncio.get_event_loop().run_in_executor(None, input, "Input: ")
                user_input = user_input.strip() # ลบช่องว่างหน้าหลัง

                # 2. เช็คคำสั่งออกจากโปรแกรม
                if user_input.lower() in ['q', 'exit']:
                    print("Disconnecting...")
                    break

                # 3. เช็คคำสั่งควบคุม Relay (ON/OFF)
                # หมายเหตุ: Relay Module ส่วนใหญ่ทำงานแบบ Active High (High=ON)
                # แต่ถ้าของคุณเป็น Active Low ให้สลับ GPIO.HIGH เป็น GPIO.LOW แทน
                if user_input.upper() == "ON":
                    GPIO.output(RELAY_PIN, GPIO.HIGH)
                    print("🔵 RELAY: Switched to NO (Active)")
                    continue  # กลับไปรอรับค่าใหม่ ไม่ส่งเข้า BLE

                if user_input.upper() == "OFF":
                    GPIO.output(RELAY_PIN, GPIO.LOW)
                    print("⚪ RELAY: Switched to NC (Inactive)")
                    continue  # กลับไปรอรับค่าใหม่ ไม่ส่งเข้า BLE

                # 4. เช็คว่าเป็นเลข 1-9 หรือไม่ (สำหรับส่ง BLE)
                if not user_input.isdigit() or not (1 <= int(user_input) <= 9):
                    print("⚠️ Invalid command. Enter ON, OFF, or 1-9.")
                    continue

                # 5. ส่งข้อมูลผ่าน BLE (เฉพาะตัวเลข 1-9)
                print(f"📡 Sending via BLE: {user_input}")
                try:
                    await client.write_gatt_char(CHARACTERISTIC_UUID, user_input.encode(), response=True)
                    print("✅ Sent successfully")
                except Exception as e:
                    print(f"❌ Failed to send: {e}")

    except Exception as e:
        print(f"Could not connect or error occurred: {e}")
    
    finally:
        # เคลียร์ค่า GPIO เมื่อจบโปรแกรมเพื่อความปลอดภัย
        GPIO.cleanup()
        print("GPIO Cleaned up.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        GPIO.cleanup() # เผื่อกรณีบังคับปิดด้วย Ctrl+C
        print("\nProgram stopped by user.")
