# Wireless ECG Monitor

Project aims to create a wireless ECG monitor using off the shelf components. It's purpose is to limit the amount of cables/wires running from the patient to the device itself - and making it easier for nurses to take care of them. The device consists of a Raspberry Pi with ADS126x High Precision ADC Hat.

## Setting up development environment (WIP)

1. Collect the hardware:
- Raspberry Pi 4 (or any other computer with Bluetooth and a screen)
- ADS126x High Precision ADC HAT

2. Connect hardware.
3. Setup SSH key authentication:
- Generate key on development machine: `ssh-keygen -t ed25519 -f key -N ""`
- Copy public key to the Raspberry Pi: 
```
    ssh $(USER)@$(IP) "mkdir -p /home/$(USER)/.ssh"
    scp key.pub $(USER)@$(IP):/home/$(USER)/.ssh/
```
- Enable key authentication by setting the following options in `/etc/ssh/sshd_config`:
```
    PubkeyAuthentication Yes
```
- Restart ssh service: `service ssh reload`
- Check the key by performing: `ssh -i key $(USER)@$(IP)`

4. Clone this repository.
5. Setup the required libraries:
```
scp -i key "wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.68.tar.gz"
scp -i key "tar zxvf bcm2835-1.68.tar.gz"
scp -i key "cd bcm2835-1.68/ && sudo su && sudo ./configure && sudo make && sudo make check && sudo make install"
```
6. Run `make` or all the actions separately: (TBD)
```
make clean
make upload
make build
make run
```

## Authors

* **Tomasz Kot** - [Koci0](https://gitlab.com/Koci0)

