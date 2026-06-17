import asyncio

import aiohttp

from midealocal.cloud import get_midea_cloud
from midealocal.discover import discover

IP = "192.168.1.192"
CLOUD_NAME = "SmartHome"
# CLOUD_NAME = "NetHome Plus"
EMAIL = "contact@oxianet.com"
PASSWORD = "oxianet@123"


async def main() -> None:
    device = next(iter(discover(ip_address=IP).values()))
    device_id = device["device_id"]

    print("IP:", device["ip_address"])
    print("Device ID:", device_id)

    async with aiohttp.ClientSession() as session:
        cloud = get_midea_cloud(CLOUD_NAME, session, EMAIL, PASSWORD)
        if not await cloud.login():
            print("cloud login failed")
            return

        _, creds = next(iter((await cloud.get_cloud_keys(device_id)).items()))
        print("Token:", creds["token"])
        print("Key:", creds["key"])


if __name__ == "__main__":
    asyncio.run(main())
