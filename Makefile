
USER := pi
IP := 192.168.55.106

HOME := /home/$(USER)
TARGET_DIR := $(HOME)/wireless_ecg

DESTINATION := $(USER)@$(IP)
SSH := ssh -i pi_ed25519 $(DESTINATION)
SCP := scp -i pi_ed25519

FILES := README.md LICENSE.md Makefile_remote src/* lib/*
TAR_NAME := wireless_ecg.tar

TARGET := wireless_ecg

all: clean upload build run

clean:
	$(SSH) rm -rf $(TARGET_DIR)

upload:
	$(SSH) mkdir -p $(TARGET_DIR)
	tar -cf $(TAR_NAME) $(FILES)
	$(SCP) -r $(TAR_NAME) $(DESTINATION):$(TARGET_DIR)
	rm -f $(TAR_NAME)
	$(SSH) tar -xvf $(TARGET_DIR)/$(TAR_NAME) -C $(TARGET_DIR)
	$(SSH) rm -f $(TARGET_DIR)/$(TAR_NAME)
	$(SSH) mv $(TARGET_DIR)/Makefile_remote $(TARGET_DIR)/Makefile

build:
	$(SSH) mkdir -p $(TARGET_DIR)/bin
	$(SSH) "cd $(TARGET_DIR) && make"

run:
	$(SSH) "sudo $(TARGET_DIR)/$(TARGET)"