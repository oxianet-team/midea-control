# Token: 9da03d4a3d20ae76ae8933549a4d1884a5ca95249dc0d913ecdd7704ae7e16c1351073a3d40e2f749de31e4d15db395d49302699fdf26ac662642db698f60c6c
# Key: f5f759ff59954ba59e727e15999716dccb4c2b2fd2a04fb1b26d070ee609197c

from asyncio import sleep
from midealocal.discover import discover
from midealocal.devices import device_selector

token = '9da03d4a3d20ae76ae8933549a4d1884a5ca95249dc0d913ecdd7704ae7e16c1351073a3d40e2f749de31e4d15db395d49302699fdf26ac662642db698f60c6c'
key = 'f5f759ff59954ba59e727e15999716dccb4c2b2fd2a04fb1b26d070ee609197c'

# Get the first device
d = list(discover(ip_address="192.168.1.192").values())[0]

# Select the device
ac = device_selector(
  name="AC",
  device_id=d['device_id'],
  device_type=d['type'],
  ip_address=d['ip_address'],
  port=d['port'],
  token=token,
  key=key,
  device_protocol=d['protocol'],
  model=d['model'],
  subtype=0,
  customize="",
)

# Connect and authenticate
ac.connect()

# Setting the temperature
ac.set_target_temperature(23.0, True)

ac.refresh_status()

print(ac.attributes.get("target_temperature"))
