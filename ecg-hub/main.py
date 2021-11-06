
import time

from threading import Thread

from bluetooth.bluez import BluetoothSocket, find_service
from bluetooth.btcommon import RFCOMM

address = "84:CC:A8:60:E5:7E"
packetSizeBytes = 8


def readFromPeripheral(socket: BluetoothSocket):
    last_read = time.time()

    try:
        while True:
            packet_data = socket.recv(8)
            if not packet_data:
                break
            unpacked_data = unpacked_data = (int.from_bytes(packet_data[0:4], "big"), int.from_bytes(
                packet_data[4:6], "big"), int.from_bytes(packet_data[6:8], "big"))
            elapsed_time = time.time() - last_read
            print(f"t-{elapsed_time * 1000}ms: {unpacked_data}")
            last_read = time.time()
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    service = find_service(address=address)[0]

    port = service["port"]
    name = service["name"]
    host = service["host"]

    print(f"Connecting to {name} on {host}...")

    bluetoothSocket = BluetoothSocket(RFCOMM)
    bluetoothSocket.connect((host, port))

    print(f"Connected.")

    btThread = Thread(target=readFromPeripheral, args=(bluetoothSocket,))

    try:
        btThread.start()
        btThread.join()
    finally:
        bluetoothSocket.close()
