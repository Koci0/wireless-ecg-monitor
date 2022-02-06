# Wireless ECG Monitor

Project aims to create a wireless ECG monitor using off the shelf components. It's purpose is to limit the amount of cables/wires running from the patient to the device itself - and making it easier for nurses to take care of them. _Node_ is a ESP32 One with AD8232 module which sends data wirelessly via Bluetooth Serial to _Hub_ (Raspberry Pi or any computer with Bluetooth) which processes data and displays it on the screen.

Project initially created as the Bachelor's Thesis at Cracow University of Technology (marked with a tag).

## Building

1. Collect hardware:
- ESP32 One (libraries used are compatible with Arduino but it was not tested)
- AD8232 (ex. from Adafruit)
- Raspberry Pi 4 (or any other computer with Bluetooth and a screen)

2. Connect hardware according to _NodeSchemePrint.png_ or according to the table below:

| AD8232 | GPIO number |
| --- | --- |
| 3.3V | 17 |
| GND | 39 |
| OUTPUT | 38 |
| LO- | 15 |
| LO+ | 11 |

3. Clone this repo.
4. Using platformio flash contents of _ecg-node_ onto _Node_.
5. Copy contents of _ecg-hub_ onto _Hub_.
6. Modify _ecg-hub/modules/bluetooth.py_ and change `address` field of `Bluetooth` class with address of _Node_.
7. Run _ecg-hub/setup.py_ (or create venv and install requirements).
8. Run _ecg-hub/run.sh_. Devices should connect automatically and start displaying data immediately.

## Authors

* **Tomasz Kot** - [Koci0](https://gitlab.com/Koci0)

