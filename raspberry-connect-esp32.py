import asyncio
from bleak import BleakClient

# ==========================================
# ใส่ MAC Address ที่คุณสแกนเจอตรงนี้ !!!
# ==========================================
ESP32_ADDRESS = "XX:XX:XX:XX:XX:XX"  # <--- แก้ตรงนี้

# UUID นี้ต้องตรงกับในโค้ด ESP32 (C++) เป๊ะๆ
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

async def main():
    print(f"Connecting to {ESP32_ADDRESS}...")

    try:
        async with BleakClient(ESP32_ADDRESS) as client:
            print(f"Connected: {client.is_connected}")

            while True:
                command = input("Enter 1 (ON), 0 (OFF), or q (Quit): ")

                if command == '1':
                    print("Sending ON command...")
                    # ส่งค่า '1' เป็น byte
                    await client.write_gatt_char(CHARACTERISTIC_UUID, b"1")

                elif command == '0':
                    print("Sending OFF command...")
                    # ส่งค่า '0' เป็น byte
                    await client.write_gatt_char(CHARACTERISTIC_UUID, b"0")

                elif command == 'q':
                    break

    except Exception as e:
        print(f"Error connection failed: {e}")

asyncio.run(main())