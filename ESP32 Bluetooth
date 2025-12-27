#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include "soc/soc.h"             
#include "soc/rtc_cntl_reg.h"    
#include "esp_bt.h"              

// ==========================================
// UUID ต้องตรงกับ Python ฝั่ง Pi Zero
// ==========================================
#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b" 
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8" 

BLEServer* pServer = NULL;
BLECharacteristic* pCharacteristic = NULL;
bool deviceConnected = false;

// Callback เช็คสถานะการเชื่อมต่อ
class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
      Serial.println("Device Connected!");
    };

    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
      Serial.println("Device Disconnected");
      // ให้เริ่มโฆษณาต่อทันทีเมื่อหลุด
      delay(500); 
      BLEDevice::startAdvertising(); 
    }
};

// Callback รับค่าจาก Python
class MyCallbacks: public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic *pCharacteristic) {
      // ดึงค่าที่ส่งมาเก็บไว้ในตัวแปร value
      String value = pCharacteristic->getValue();
      
      if (value.length() > 0) {
        Serial.print("Received Value: ");
        Serial.println(value); // พิมพ์ค่าที่รับได้ออกมาดูทาง Serial Monitor

        // ==========================================================
        // พื้นที่สำหรับเขียน Logic ของคุณเอง
        // ตัวแปร 'value' คือข้อมูลที่ส่งมาจาก Python
        // เช่น ถ้าส่งมาเป็น "FW" คุณก็เขียนเงื่อนไขเช็คที่นี่ได้เลย
        // ==========================================================
        
      }
    }
};

void setup() {
  // 1. ปิด Brownout Detector (ป้องกันรีเซ็ตเมื่อไฟตก)
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);

  Serial.begin(115200);

  // 2. Delay ให้ไฟนิ่งก่อนเริ่มทำงาน
  Serial.println("Waiting for power to stabilize...");
  delay(2000); 

  // 3. เริ่มต้น Bluetooth และ ลดกำลังส่ง
  BLEDevice::init("ESP32_WPT_Device");
  
  // ลดกำลังส่งลงเพื่อประหยัดไฟและลดสัญญาณรบกวน
  esp_bredr_tx_power_set(ESP_PWR_LVL_N0, ESP_PWR_LVL_P3); 

  // สร้าง Server และ Service
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());
  BLEService *pService = pServer->createService(SERVICE_UUID);

  // สร้าง Characteristic
  pCharacteristic = pService->createCharacteristic(
                      CHARACTERISTIC_UUID,
                      BLECharacteristic::PROPERTY_READ   |
                      BLECharacteristic::PROPERTY_WRITE
                    );

  pCharacteristic->setCallbacks(new MyCallbacks());
  pCharacteristic->addDescriptor(new BLE2902());

  // เริ่ม Service
  pService->start();

  // เริ่มโฆษณา (Advertising) เพื่อให้ Pi หาเจอ
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(false);
  pAdvertising->setMinPreferred(0x0); 
  BLEDevice::startAdvertising();
  
  Serial.println("Waiting for client connection...");
}

void loop() {
  // ไม่ต้องทำอะไร รอรับค่าจาก Callback อย่างเดียว
  delay(100); 
}
