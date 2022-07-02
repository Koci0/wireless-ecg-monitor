
USER := pi
IP := 192.168.55.102

HOME := /home/$(USER)
DIR := $(HOME)/wireless_ecg

DESTINATION := $(USER)@$(IP)
SSH := ssh -i pi_ed25519 $(DESTINATION)
SCP := scp -i pi_ed25519

FILES := README.md LICENSE.md Makefile

all: clean upload build run

clean:
	$(SSH) rm -rf $(DIR)

upload:
	$(SSH) mkdir $(DIR)
	$(SCP) -r $(FILES) $(DESTINATION):$(DIR)

build:
	echo "Build"

run:
	echo "Run"