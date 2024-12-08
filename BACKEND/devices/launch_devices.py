import sys
from devices.device_handler import DeviceHandler


def is_running_in_venv():
    return sys.prefix != getattr(sys, 'base_prefix', sys.prefix)


def main():
    if not is_running_in_venv():
        print("Not running inside a virtual environment.")
        raise EnvironmentError("The program must be run inside a virtual environment.")

    device_handler = DeviceHandler()
    device_handler.start()


if __name__ == "__main__":
    main()
