
import asyncio
from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError
import time

address = "84:CC:A8:60:E5:7E"
target_uuid = "00002a3d-fc88-4a2f-a932-b65010875819"

uuidLeadsCharacteristic = ""
uuidEcgTimeCharacteristic = ""
uuidEcgValueCharacteristic = ""

last_read = 0

async def scan():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)

async def findCharacteristics(client: BleakClient):
    global uuidLeadsCharacteristic, uuidEcgTimeCharacteristic, uuidEcgValueCharacteristic

    services = client.get_services()
    for s in services:
        print(f"Service {s} characteristics:")
        for c in s.characteristics:
            print("\t" + c)

async def main():
    global last_read

    device = await BleakScanner.find_device_by_address(address, timeout=10.0)
    if not device:
        raise BleakError(f"Failed to find a device {address}")

    try:
        async with BleakClient(device) as client:
            if not uuidLeadsCharacteristic or not uuidEcgTimeCharacteristic or not uuidEcgValueCharacteristic:
                asyncio.run(findCharacteristics(client))
            else:
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
                        
                        leadsCharacteristic = client.services.get_characteristic(uuidLeadsCharacteristic)
                        ecgTimeCharacteristic = client.services.get_characteristic(uuidEcgTimeCharacteristic)
                        ecgValueCharacteristic = client.services.get_characteristic(uuidEcgValueCharacteristic)
                        last_read = 0
                        while True:
                            try:
                                leadsData = await client.read_gatt_char(leadsCharacteristic)
                                ecgTimeData = await client.read_gatt_char(ecgTimeCharacteristic)
                                ecgValueData = await client.read_gatt_char(ecgValueCharacteristic)
                                elapsed_time = time.time() - last_read
                                print(f"T-{elapsed_time * 1000}ms:")
                                print(f"Leads data: {leadsData}")
                                print(f"ECG Time data: {ecgTimeData}")
                                print(f"ECG Value data: {ecgValueData}")
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
