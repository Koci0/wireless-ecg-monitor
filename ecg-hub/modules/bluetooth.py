
import sys

from queue import Full, Queue
from threading import Event, Thread

from bluetooth.bluez import BluetoothSocket, find_service
from bluetooth.btcommon import RFCOMM, BluetoothError

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Bluetooth:
    address = "84:CC:A8:60:E5:7E"
    packetSizeBytes = 8

    def __init__(self, dataQueue: Queue, stopEvent: Event, address=None, packetSizeBytes=None):
        if address:
            self.address = address
        if packetSizeBytes:
            self.packetSizeBytes = packetSizeBytes

        self.dataQueue = dataQueue
        self.stopEvent = stopEvent

        self.thread = Thread(target=self.receiveFromPeripheral)

    def connect(self):
        service = find_service(address=self.address)[0]

        port = service["port"]
        name = service["name"]
        host = service["host"]

        logger.info(f"Connecting to {name} on {host}...")
        self.socket = BluetoothSocket(RFCOMM)
        self.socket.connect((host, port))
        logger.info(f"Connected.")

    def start(self):
        logger.info("Thread starting.")
        self.thread.start()

    def stop(self):
        logger.info("Thread stopping.")
        self.thread.join()

    def receiveFromPeripheral(self):
        while not self.stopEvent.is_set():
            packet_data = self.socket.recv(8)
            if not packet_data:
                break
            try:
                self.dataQueue.put(packet_data, timeout=0.005)
            except Full:
                logger.warning("Queue timeout!")
