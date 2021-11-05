
import time

import bluetooth

address = "84:CC:A8:60:E5:7E"

last_read = 0


if __name__ == "__main__":
    service = bluetooth.find_service(address=address)[0]

    port = service["port"]
    name = service["name"]
    host = service["host"]

    print(f"Connecting to {name} on {host}...")

    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((host, port))

    print(f"Connected.")
    try:
        while True:
            packet_data = sock.recv(1024)
            if not packet_data:
                break
            elapsed_time = time.time() - last_read
            unpacked_data = unpacked_data = (int.from_bytes(packet_data[0:4], "big"), int.from_bytes(
                packet_data[4:6], "big"), int.from_bytes(packet_data[6:8], "big"))
            print(f"t-{elapsed_time * 1000}ms: {unpacked_data}")
            last_read = time.time()
    except OSError as error:
        print(f"OSError: {error}")
    except KeyboardInterrupt:
        pass
    finally:
        sock.close()
