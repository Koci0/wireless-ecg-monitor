
#include <Arduino.h>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>

const char *nameOfPeripheral = "Heart Rate Monitor";
const char *uuidOfService = "00001800-fc88-4a2f-a932-b65010875819";
const char *uuidOfCharacteristic = "00002A3D-fc88-4a2f-a932-b65010875819";

BLEServer *pServer;
BLEService *pService;
BLECharacteristic *pCharacteristic;

void setup()
{
    Serial.begin(115200);
    while (not Serial)
        ;
    Serial.println("Staring BLE...");
    BLEDevice::init(nameOfPeripheral);
    pServer = BLEDevice::createServer();
    pService = pServer->createService(uuidOfService);
    pCharacteristic = pService->createCharacteristic(
        uuidOfCharacteristic,
        BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_WRITE);
    pCharacteristic->setValue("Hello world");
    pService->start();
    BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
    pAdvertising->addServiceUUID(uuidOfService);
    pAdvertising->setScanResponse(true);
    BLEDevice::startAdvertising();

    Serial.println("BLE server active, waiting for connections...");
}

void loop()
{
    while (true)
    {
        auto data = pCharacteristic->getValue();
        Serial.print("getValue: ");
        Serial.println(data.c_str());
        delay(1000);
    }
}