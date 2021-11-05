
#include <Arduino.h>

#include "BluetoothSerial.h"

#define DEBUG 0

BluetoothSerial btSerial;


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

    Serial.println("Preparing Bluetooth Serial...");
    btSerial.begin("ESP32_ECG_Monitor");
    
    Serial.println("Setup finished.");
}

void loop()
{
    updatePacketValue();
    btSerial.write(packet, packetSize);
}