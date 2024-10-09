import evdev

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    print(f'Path: {device.path}, Name: {device.name}')
