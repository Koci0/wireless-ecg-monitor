
import asyncio
from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError
import time

address = "84:CC:A8:60:E5:7E"
target_uuid = "00002a3d-fc88-4a2f-a932-b65010875819"

last_read = 0

async def scan():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)
    
async def main():
    global last_read

    device = await BleakScanner.find_device_by_address(address, timeout=10.0)
    if not device:
        raise BleakError(f"Failed to find a device {address}")

    try:
        async with BleakClient(device) as client:
            running = True
            while running:
                try:
                    if not client.is_connected:
                        print("Client not connected, trying to connect...")
                        try:
                            await client.connect()
                        except Exception as e:
                            print(f"Got exception while trying to connect: {e}")
                    
                        print("Connected")
                        services = await client.get_services()
                        for s in services:
                            print(f"{s} - characteristics:")
                            for c in s.characteristics:
                                print(f"\tc")
                    
                    characteristic = client.services.get_characteristic(target_uuid)
                    last_read = 0
                    while True:
                        try:
                            data = await client.read_gatt_char(characteristic)
                            elapsed_time = time.time() - last_read
                            print(f"T-{elapsed_time * 1000}ms:\t{data}")
                            last_read = time.time()
                        except Exception as e:
                            print(f"Got exception while reading data: {e}")
                            print("Breaking!")
                            break
                except Exception as e:
                    print(f"Got exception in main loop: {e}")
                finally:
                    client.disconnect()
                    client.unpair()
    except Exception as e:
        print(f"Got exception in client context: {e}")

if __name__ == "__main__":
    asyncio.run(main())
