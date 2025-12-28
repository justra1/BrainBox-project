import asyncio
from bleak import BleakClient

# --- การตั้งค่า ---
DEVICE_ADDRESS = "6C:C8:40:58:AE:62"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

async def main():
    print(f"Connecting to {DEVICE_ADDRESS} ...")

    try:
        async with BleakClient(DEVICE_ADDRESS) as client:
            print(f"Connected: {client.is_connected}")
            print("-" * 30)
            print("Type a number (1-9) and press ENTER to send.")
            print("Type 'q' or 'exit' to quit.")
            print("-" * 30)

            while True:
                # 1. รอรับค่า Input จากคีย์บอร์ด (ใช้ run_in_executor เพื่อไม่ให้บล็อกการเชื่อมต่อ BLE)
                # หมายเหตุ: การใช้ input() ธรรมดาใน async บางครั้งอาจทำให้ connection หลุดถ้าจอนาน
                # แต่วิธีนี้ง่ายที่สุดสำหรับการทดสอบ
                user_input = await asyncio.get_event_loop().run_in_executor(None, input, "Input (1-9): ")

                # เช็คเงื่อนไขออกโปรแกรม
                if user_input.lower() in ['q', 'exit']:
                    print("Disconnecting...")
                    break

                # 2. ตรวจสอบว่าเป็นเลข 1-9 หรือไม่ (ถ้าไม่ซีเรียส ลบส่วนเช็คนี้ออกได้)
                if not user_input.isdigit() or not (1 <= int(user_input) <= 9):
                    print("⚠️ Please enter a number between 1 and 9 only.")
                    continue

                # 3. ส่งข้อมูล
                print(f"Sending: {user_input}")
                try:
                    await client.write_gatt_char(CHARACTERISTIC_UUID, user_input.encode(), response=True)
                    print("✅ Sent successfully")
                except Exception as e:
                    print(f"❌ Failed to send: {e}")
                    # พยายามเชื่อมต่อใหม่หรือจัดการ Error ตามต้องการ

    except Exception as e:
        print(f"Could not connect: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
