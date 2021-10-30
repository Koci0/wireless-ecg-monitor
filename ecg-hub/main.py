
import asyncio
import time

from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError
from threading import Thread

address = "84:CC:A8:60:E5:7E"

uuidService = "00001006-fc88-4a2f-a932-b65010875819"
uuidCharacteristic = "00001006-fc88-4a2f-a932-b65010875820"

last_read = 0


async def bleak_main():
    global last_read

    device = await BleakScanner.find_device_by_address(address, timeout=10.0)
    if not device:
        raise BleakError(f"Failed to find a device {address}")

    try:
        async with BleakClient(device) as client:
            if not uuidCharacteristic:
                raise ValueError("UUID is not present!")
            else:
                running = True
                while running:
                    try:
                        if not client.is_connected:
                            print("Client not connected, trying to connect...")
                            try:
                                await client.connect()
                            except Exception as e:
                                print(
                                    f"Got exception while trying to connect: {e}")

                            print("Connected")
                            services = await client.get_services()
                            for s in services:
                                print(f"{s} - characteristics:")
                                for c in s.characteristics:
                                    print(f"\t{c}")

                        characteristic = client.services.get_characteristic(
                            uuidCharacteristic)
                        last_read = 0
                        while True:
                            try:
                                packet_data = await client.read_gatt_char(characteristic)
                                unpacked_data = (int.from_bytes(packet_data[0:4], "big"), int.from_bytes(packet_data[4:6], "big"), int.from_bytes(packet_data[6:8], "big"))
                                elapsed_time = time.time() - last_read
                                print(f"T-{elapsed_time * 1000}ms\nPacket: {unpacked_data}")
                                last_read = time.time()
                            except Exception as e:
                                print(f"Got exception while reading data: {e}")
                                print("Breaking!")
                                break
                    except Exception as e:
                        print(f"Got exception in main loop: {e}")
                    finally:
                        await client.disconnect()
                        await client.unpair()
    except Exception as e:
        print(f"Got exception in client context: {e}")

if __name__ == "__main__":

    # Setup bleak thread
    asyncio_loop = asyncio.get_event_loop()
    def bleak_thread(loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()
    thread = Thread(target=bleak_thread, args=(asyncio_loop,))
    thread.start()

    # Run bleak function
    asyncio.run_coroutine_threadsafe(bleak_main(), asyncio_loop)
