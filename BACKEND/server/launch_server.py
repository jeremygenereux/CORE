import sys
from .server import start_server

def is_running_in_venv():
    return sys.prefix != getattr(sys, 'base_prefix', sys.prefix)


def main():
    if not is_running_in_venv():
        print("Not running inside a virtual environment.")
        raise EnvironmentError("The program must be run inside a virtual environment.")

    start_server()


if __name__ == "__main__":
    main()
