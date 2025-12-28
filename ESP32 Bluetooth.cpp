#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include "soc/soc.h"             
#include "soc/rtc_cntl_reg.h"    

#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b" 
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8" 

// กำหนดขา LED (ถ้าบอร์ด ESP32 ทั่วไปมักจะเป็นขา 2)
#define LED_PIN 2 

BLEServer* pServer = NULL;
BLECharacteristic* pCharacteristic = NULL;
bool deviceConnected = false;

// ---------------------------------------------------------
// 1. พื้นที่สำหรับเขียนฟังก์ชันแยก (Functions Zone)
// ---------------------------------------------------------

// ฟังก์ชันที่จะทำงานเมื่อได้รับเลข 1
void actionNumberOne() {
  Serial.println(">> Executing Function 1: Turn ON LED");
  digitalWrite(LED_PIN, HIGH); // ตัวอย่าง: สั่งเปิดไฟ
  // ใส่โค้ดอื่นๆ ที่ต้องการให้ทำเมื่อกด 1 ที่นี่
}

// ฟังก์ชันที่จะทำงานเมื่อได้รับเลข 2
void actionNumberTwo() {
  Serial.println(">> Executing Function 2: Turn OFF LED");
  digitalWrite(LED_PIN, LOW); // ตัวอย่าง: สั่งปิดไฟ
}

// ฟังก์ชันที่จะทำงานเมื่อได้รับเลข 9 (ตัวอย่างเพิ่มเติม)
void actionNumberNine() {
  Serial.println(">> Executing Function 9: Say Hello");
}

// ---------------------------------------------------------

class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
      Serial.println("Device Connected");
    };
    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
      Serial.println("Device Disconnected");
      delay(500); 
      BLEDevice::startAdvertising(); 
    }
};

class MyCallbacks: public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic *pCharacteristic) {
      
      // --- แก้ไขตรงนี้ ---
      // เปลี่ยนจาก std::string เป็น String
      String value = pCharacteristic->getValue(); 

      if (value.length() > 0) {
        // แสดงค่าที่ได้รับทาง Serial Monitor
        Serial.print("Received: ");
        Serial.println(value); // Arduino String สั่ง print ได้เลย

        // ตรวจสอบค่าและเรียกฟังก์ชัน
        char command = value[0]; 

        if (command == '1') {
           actionNumberOne(); 
        }
        else if (command == '2') {
           actionNumberTwo(); 
        }
        else if (command == '9') {
           actionNumberNine();
        }
        else {
           Serial.println("Unknown command");
        }
      }
    }
};

void setup() {
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);
  Serial.begin(115200);

  // ตั้งค่าขา LED
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  BLEDevice::init("ESP32_WPT_Device");
  
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());
  BLEService *pService = pServer->createService(SERVICE_UUID);

  pCharacteristic = pService->createCharacteristic(
                      CHARACTERISTIC_UUID,
                      BLECharacteristic::PROPERTY_READ   |
                      BLECharacteristic::PROPERTY_WRITE  |
                      BLECharacteristic::PROPERTY_WRITE_NR 
                    );

  pCharacteristic->setCallbacks(new MyCallbacks());
  pCharacteristic->addDescriptor(new BLE2902());

  pService->start();

  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(false);
  pAdvertising->setMinPreferred(0x0); 
  BLEDevice::startAdvertising();
  
  Serial.println("Ready. Waiting for command...");
}

void loop() {
  // ใน Loop ปล่อยว่างไว้ หรือใส่ delay เล็กน้อย
  // การทำงานหลักจะเกิดขึ้นเมื่อมีการ "Write" เข้ามา (Event Driven)
  delay(1000); 
}
