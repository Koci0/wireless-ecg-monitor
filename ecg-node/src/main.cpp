
#include <Arduino.h>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>

#define DEBUG 0

typedef int lead_t;
typedef unsigned int ecg_time_t;
typedef int ecg_value_t;

const char *peripheralName = "Heart Rate Monitor";
const char *uuidService = "00001006-fc88-4a2f-a932-b65010875819";
// Leads connected/disconnected
const char *uuidLeadsCharacteristic = "00001006-fc88-4a2f-a932-b65010875820"; // 123
// ECG
const char *uuidEcgTimeCharacteristic = "00001006-fc88-4a2f-a932-b65010875821";  // 456
const char *uuidEcgValueCharacteristic = "00001006-fc88-4a2f-a932-b65010875822"; // 789

BLEServer *pServer;
BLEService *pService;
BLECharacteristic *pLeadsCharacteristic;
BLECharacteristic *pEcgTimeCharacteristic;
BLECharacteristic *pEcgValueCharacteristic;

lead_t getLeadsData()
{
    return 1;
}

ecg_time_t getEcgTimeData()
{
    return millis();
}

ecg_value_t getEcgValueData()
{
    return 3;
}

void setup()
{
    Serial.begin(115200);
    while (not Serial)
        ;
    Serial.println("Staring BLE...");
    BLEDevice::init(peripheralName);
    pServer = BLEDevice::createServer();
    pService = pServer->createService(uuidService);

    // Setup Leads
    Serial.println("Setting up Leads");
    pLeadsCharacteristic = pService->createCharacteristic(
        uuidLeadsCharacteristic,
        BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_WRITE);
    pLeadsCharacteristic->setValue("123");

    // Setup Ecg
    Serial.println("Setting up ECG");
    pEcgTimeCharacteristic = pService->createCharacteristic(
        uuidEcgTimeCharacteristic,
        BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_WRITE);
    pEcgTimeCharacteristic->setValue("456");
    pEcgValueCharacteristic = pService->createCharacteristic(
        uuidEcgValueCharacteristic,
        BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_WRITE);
    pEcgValueCharacteristic->setValue("789");

    pService->start();

    BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
    pAdvertising->addServiceUUID(uuidService);
    pAdvertising->setScanResponse(true);
    BLEDevice::startAdvertising();

    Serial.println("BLE server active, waiting for connections...");
}

void loop()
{
    while (true)
    {
        auto leadsData = getLeadsData();
        auto ecgTimeData = getEcgTimeData();
        auto ecgValueData = getEcgValueData();

        pLeadsCharacteristic->setValue(leadsData);
        pEcgTimeCharacteristic->setValue(ecgTimeData);
        pEcgValueCharacteristic->setValue(ecgValueData);

        #if DEBUG == 1
        Serial.print("#################### ");
        Serial.println(millis());
        Serial.print("Leads:\t\t");
        Serial.println(*pLeadsCharacteristic->getData());
        Serial.print("EcgTime:\t");
        Serial.println(*pEcgTimeCharacteristic->getData());
        Serial.print("EcgValue:\t");
        Serial.println(*pEcgValueCharacteristic->getData());
        Serial.println();

        delay(3000);
        #endif
    }
}