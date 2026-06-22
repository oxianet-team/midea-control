import time
import sys
from enum import Enum
from datetime import datetime
from midealocal.discover import discover
from midealocal.devices import device_selector
from midealocal.devices import MideaDevice

# {'device_id': 152832117819720, 'type': 172, 'ip_address': '192.168.1.192', 'port
# ': 6444, 'model': '0L646802', 'sn': '0000AC5410L646802B30708102100000', 'protoco
# l': 3}

class PowerState(Enum):
    ON = "on"
    OFF = "off"


def _close_device(device: MideaDevice) -> None:
    print("Closing connection.")
    try:
        device.close()
    except Exception as close_exc:
        print(f"Warning: failed to close connection: {close_exc}")

def find_ac(token: str, key: str)-> MideaDevice|bool:
    print("Discovering devices on the network...")
    discover_results = list(discover().values())

    d = {}

    for device in discover_results:
        if device['device_id'] == 152832117819720:
            d = device

    if d == {}:
        print("No device found on the network! ")
        return False

    print("Device found: " + d['model'] + " with IP " + d['ip_address'])

    return device_selector(
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

def change_state_power_ac(device: MideaDevice, state: PowerState) -> None:
    desired_on = state is PowerState.ON
    opened = False

    try:
        device.connect(check_protocol=True)
        device.open()
        opened = True

        print("Connecting to the device, retrieving current state...")
        time.sleep(5)

        is_on = bool(device._attributes.get("power"))
        if is_on == desired_on:
            print(f"AC is already {state.value}")
            return

        device.set_attribute("power", desired_on)
        time.sleep(2)
        print(f"The state of the AC has been changed successfully to {state.value}")
    except Exception as exc:
        if opened == False:
            print("Failed to connect to the device.")
        else:
            print(f"Failed to change AC power state ({state.value}): {exc}")
        raise
    finally:
        if opened:
            _close_device(device)

def main():
    state = sys.argv[1]

    try:
        state = PowerState(state)
    except ValueError:
        print("Parameter does not exist.")
        return 

    device = find_ac(
    token= '9da03d4a3d20ae76ae8933549a4d1884a5ca95249dc0d913ecdd7704ae7e16c1351073a3d40e2f749de31e4d15db395d49302699fdf26ac662642db698f60c6c',
    key= 'f5f759ff59954ba59e727e15999716dccb4c2b2fd2a04fb1b26d070ee609197c'
    )

    if isinstance(device, MideaDevice) == False:
        return

    change_state_power_ac(device, state)

if len(sys.argv) == 2:
    main()
else:
    print("Usage: python control-midea.py <on|off>")
