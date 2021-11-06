
from time import sleep
from threading import Event, Thread
from queue import Empty, Full, Queue

from bluetooth.bluez import BluetoothSocket, find_service
from bluetooth.btcommon import RFCOMM

address = "84:CC:A8:60:E5:7E"
packetSizeBytes = 8

dataQueue = Queue()
stopEvent = Event()


def receiveFromPeripheral(socket: BluetoothSocket):
    while not stopEvent.is_set():
        packet_data = socket.recv(8)
        if not packet_data:
            break
        try:
            dataQueue.put(packet_data, timeout=0.005)
        except Full:
            print("Queue timeout!")


def readFromQueue():
    while not stopEvent.is_set():
        try:
            raw_data = dataQueue.get_nowait()
            unpacked_data = (int.from_bytes(raw_data[0:4], "big"), int.from_bytes(
                raw_data[4:6], "big"), int.from_bytes(raw_data[6:8], "big"))
            print(unpacked_data)
        except Empty:
            pass


if __name__ == "__main__":
    service = find_service(address=address)[0]

    port = service["port"]
    name = service["name"]
    host = service["host"]

    print(f"Connecting to {name} on {host}...")
    btSocket = BluetoothSocket(RFCOMM)
    btSocket.connect((host, port))
    print(f"Connected.")

    btThread = Thread(target=receiveFromPeripheral, args=(btSocket,))
    queueThread = Thread(target=readFromQueue, args=())

    btThread.start()
    queueThread.start()

    try:
        while btThread.is_alive() or queueThread.is_alive():
            sleep(3)
    except KeyboardInterrupt:
        stopEvent.set()
    finally:
        btThread.join()
        queueThread.join()
        btSocket.close()
