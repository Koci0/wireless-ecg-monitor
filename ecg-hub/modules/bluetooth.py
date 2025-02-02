
import sys

from queue import Full, Queue
from threading import Event, Thread

from bluetooth.bluez import BluetoothSocket, find_service
from bluetooth.btcommon import RFCOMM, BluetoothError

from modules.logger import Logger
logger = Logger()


class Bluetooth:

    address = "84:CC:A8:60:E5:7E"
    packetSizeBytes = 8
    maxRetries = 3

    def __init__(self, stopEvent: Event, dataQueue: Queue, address=None, packetSizeBytes=None):
        if address:
            self.address = address
        if packetSizeBytes:
            self.packetSizeBytes = packetSizeBytes
        self.socket = BluetoothSocket(RFCOMM)

        self.dataQueue = dataQueue
        self.stopEvent = stopEvent

        self.thread = Thread(target=self.receiveFromPeripheral)

    def connect(self) -> bool:
        try:
            service = find_service(address=self.address)[0]
        except:
            print("Failed to find services. Check device and address.")
            sys.exit(1)

        port = service["port"]
        name = service["name"]
        host = service["host"]

        logger.info(f"Connecting to {name} on {host}...")
        try:
            self.socket.connect((host, port))
        except:
            return False
        logger.info(f"Connected.")
        return True

    def start(self):
        logger.info("Thread starting.")
        self.thread.start()

    def stop(self):
        logger.info("Thread stopping.")
        self.socket.close()

    def receiveFromPeripheral(self):
        while not self.stopEvent.is_set():
            try:
                packet_data = self.socket.recv(8)
            except BluetoothError as error:
                print(f"Failed to receive data: {error}")
                for _ in range(self.maxRetries):
                    if self.connect():
                        break
                else:
                    print("Failed to reconnect. Exit!")
                    sys.exit(1)

            if not packet_data:
                break

            try:
                self.dataQueue.put(packet_data, timeout=0.005)
            except Full:
                logger.warning("Queue timeout!")
        
        self.stop()
