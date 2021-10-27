
#include <Arduino.h>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>

typedef int lead_t;
typedef int ecg_t;

const char *peripheralName= "Heart Rate Monitor";
const char *uuidService = "00001800-fc88-4a2f-a932-b65010875819";
// Leads connected/disconnected
const char *uuidLeadsCharacteristic = "00002A3D-fc88-4a2f-a932-b65010875819"; // 123
// ECG
const char *uuidEcgTimeCharacteristic = ""; // 456
const char *uuidEcgValueCharacteristic = ""; // 789

BLEServer *pServer;
BLEService *pService;
BLECharacteristic *pLeadsCharacteristic;
BLECharacteristic *pEcgTimeCharacteristic;
BLECharacteristic *pEcgValueCharacteristic;

lead_t getLeadsData()
{
    return 1;
}

time_t getEcgTimeData()
{
    return 2;
}

ecg_t getEcgValueData()
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
        BLECharacteristic::PROPERTY_WRITE);

    // Setup Ecg
    Serial.println("Setting up ECG");
    pEcgTimeCharacteristic = pService->createCharacteristic(
        uuidEcgTimeCharacteristic,
        BLECharacteristic::PROPERTY_WRITE);
    pEcgValueCharacteristic = pService->createCharacteristic(
        uuidEcgValueCharacteristic,
        BLECharacteristic::PROPERTY_WRITE);

    pService->start();

    BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
    pAdvertising->addServiceUUID(uuidService);
    pAdvertising->setScanResponse(true);
    BLEDevice::startAdvertising();

    Serial.println("BLE server active, waiting for connections...");
}

void loop()
{
    Serial.println("####################");
    while (true)
    {
        lead_t leadsData = getLeadsData();
        time_t ecgTimeData = getEcgTimeData();
        ecg_t ecgValueData = getEcgValueData();

        Serial.print("Leads:\t");
        Serial.println(leadsData);
        Serial.print("EcgTime:\t");
        Serial.println(ecgTimeData);
        Serial.print("EcgValue:\t");
        Serial.println(ecgValueData);
        Serial.println("####################");

        delay(1000);
    }
}