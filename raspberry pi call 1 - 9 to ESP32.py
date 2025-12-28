import asyncio
from bleak import BleakClient

ESP32_ADDRESS = "6C:C8:40:58:AE:62" # <--- ใส่ MAC ของคุณ
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

# ========================================================
# ฟังก์ชันนี้จะทำงานอัตโนมัติ เมื่อ ESP32 ส่งข้อมูลกลับมา
# ========================================================
def notification_handler(sender, data):
    # data ที่ได้มาจะเป็น byte ต้อง decode เป็น string
    received_string = data.decode()
    print(f"\n[ESP32 says]: {received_string}")
    # print สวยๆ เพื่อไม่ให้ทับกับช่อง input (แต่ก็ยังทับบ้างนิดหน่อย)
    print("Enter command (1-9 or q): ", end="", flush=True)

async def main():
    print(f"Connecting to {ESP32_ADDRESS}...")

    try:
        async with BleakClient(ESP32_ADDRESS) as client:
            print(f"Connected: {client.is_connected}")
            
            # ----------------------------------------------------
            # เริ่มเปิดรับข้อมูล (Subscribe to Notifications)
            # ----------------------------------------------------
            await client.start_notify(CHARACTERISTIC_UUID, notification_handler)

            print("------------------------------------------------")
            print("Listening for sensor data... (Input works normally)")
            print("------------------------------------------------")

            while True:
                # หมายเหตุ: การใช้ input() จะหยุดรอ user พิมพ์
                # แต่ข้อมูลจาก sensor จะยังคงเด้งเข้ามาแทรกได้ (อาจจะทำให้หน้าจอเลอะเทอะนิดหน่อย)
                command = input("Enter command (1-9 or q): ")

                if command.lower() == 'q':
                    break
                
                elif command in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    # ส่งค่าไปหา ESP32
                    await client.write_gatt_char(CHARACTERISTIC_UUID, command.encode())
                
                else:
                    print("Invalid input")

            # ก่อนจบโปรแกรม ยกเลิกการรับข้อมูล
            await client.stop_notify(CHARACTERISTIC_UUID)

    except Exception as e:
        print(f"Error: {e}")

asyncio.run(main())
