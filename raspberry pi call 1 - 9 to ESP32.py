import asyncio
from bleak import BleakScanner, BleakClient

# ==========================================
# UUID ต้องตรงกับ ESP32 เป๊ะๆ
# ==========================================
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

async def main():
    print("Searching for ESP32 with specific Service UUID...")
    
    # 1. ค้นหาอุปกรณ์ที่มี Service UUID ที่เรากำหนด
    # วิธีนี้ชัวร์กว่าการหาชื่อ เพราะชื่ออาจซ้ำหรือเปลี่ยนได้
    device = await BleakScanner.find_device_by_filter(
        lambda d, ad: SERVICE_UUID.lower() in ad.service_uuids
    )

    if not device:
        print(f"Not found device with Service UUID: {SERVICE_UUID}")
        return

    print(f"Found Device: {device.name} ({device.address})")
    print("Connecting...")

    # 2. เชื่อมต่อ
    async with BleakClient(device.address) as client:
        print(f"Connected: {client.is_connected}")

        # วนลูปส่งค่า 1 ถึง 9
        for i in range(1, 10):
            value_to_send = str(i) # แปลงตัวเลขเป็น String
            print(f"Sending: {value_to_send}")

            try:
                # ---------------------------------------------------------
                # จุดสำคัญแก้ Error "Operation is not supported"
                # ---------------------------------------------------------
                # เราต้องระบุ Characteristic UUID (ไม่ใช่ Service)
                # และ response=True คือการเขียนแบบรอการยืนยัน (Write With Response)
                await client.write_gatt_char(
                    CHARACTERISTIC_UUID, 
                    value_to_send.encode(), # ต้องแปลง string เป็น bytes
                    response=True 
                )
            except Exception as e:
                print(f"Error sending {value_to_send}: {e}")
                # ถ้า response=True พัง ให้ลอง response=False (Write Without Response)
                try:
                    print("Retrying with response=False...")
                    await client.write_gatt_char(
                        CHARACTERISTIC_UUID, 
                        value_to_send.encode(), 
                        response=False
                    )
                except Exception as e2:
                    print(f"Failed again: {e2}")

            await asyncio.sleep(1) # หน่วงเวลา 1 วินาทีก่อนส่งค่าต่อไป

        print("Finished sending values 1-9")
        # เมื่อจบ block 'async with' มันจะ disconnect ให้อัตโนมัติ

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program stopped by user")
