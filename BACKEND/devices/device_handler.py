from openant.easy.node import Node
from openant.devices import ANTPLUS_NETWORK_KEY
from openant.devices.heart_rate import HeartRate, HeartRateData


class DeviceHandler:
    def __init__(self, device_id=39724):
        self.device_id = device_id
        self.node = Node()
        self.device = None

    def setup_device(self):
        self.node.set_network_key(0x00, ANTPLUS_NETWORK_KEY)
        self.device = HeartRate(self.node, device_id=self.device_id)
        self.device.on_found = self.on_found
        self.device.on_device_data = self.on_device_data

    def on_found(self):
        print(f"Device {self.device} found and receiving")

    def on_device_data(self, page: int, page_name: str, data):
        if isinstance(data, HeartRateData):
            print(f"Heart rate update {data.heart_rate} bpm")

    def start(self):
        self.setup_device()
        try:
            print(f"Starting {self.device}, press Ctrl-C to finish")
            self.node.start()
        except KeyboardInterrupt:
            print("Closing ANT+ device...")
        finally:
            self.device.close_channel()
            self.node.stop()