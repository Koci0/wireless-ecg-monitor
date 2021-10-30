
#include <Arduino.h>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>

#define DEBUG 0

const char *peripheralName = "Heart Rate Monitor";
const char *uuidService = "00001006-fc88-4a2f-a932-b65010875819";
const char *uuidCharacteristic = "00001006-fc88-4a2f-a932-b65010875820";

BLEServer *pServer;
BLEService *pService;
BLECharacteristic *pCharacteristic;

const unsigned int LO_POS = 11;
const unsigned int LO_NEG = 15;
const unsigned int ADC = 33;

const unsigned short packetSize = 8;
uint8_t packet[packetSize];

uint16_t getLeadsData()
{
    return digitalRead(LO_POS) & digitalRead(LO_NEG);
}

unsigned long getEcgTimeData()
{
    return millis();
}

uint16_t getEcgValueData()
{
    return analogRead(ADC);
}

void updatePacketValue()
{
    auto time = getEcgTimeData();
    packet[0] = time >> 24;
    packet[1] = time >> 16;
    packet[2] = time >> 8;
    packet[3] = time >> 0;

    auto leads = getLeadsData();
    packet[4] = leads >> 8;
    packet[5] = leads >> 0;

    auto ecg = getEcgValueData();
    packet[6] = ecg >> 8;
    packet[7] = ecg >> 0;

    #if DEBUG == 1
    Serial.printf("Time: %d\n", time);
    Serial.printf("Leads: %d\n", leads);
    Serial.printf("ECG: %d\n", ecg);
    #endif
}

void setup()
{
    Serial.begin(115200);
    while (not Serial)
        ;

    Serial.println("Preparing ADS...");
    pinMode(LO_POS, INPUT);
    pinMode(LO_NEG, INPUT);

    Serial.println("Starting BLE...");
    BLEDevice::init(peripheralName);
    pServer = BLEDevice::createServer();
    pService = pServer->createService(uuidService);

    Serial.println("Setting up BLE service");
    pCharacteristic = pService->createCharacteristic(
        uuidCharacteristic,
        BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_WRITE);
    pCharacteristic->setValue("123");
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
        updatePacketValue();
        pCharacteristic->setValue(packet, packetSize);

        #if DEBUG == 1
        Serial.print("#################### ");
        Serial.println(millis());
        for (size_t i = 0; i < packetSize; i++)
        {
            Serial.print(packet[i]);
            Serial.print(" ");
        }
        Serial.println();

        delay(3000);
        #endif
    }
}