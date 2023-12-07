from zk import ZK, const
import logging

class ZKDeviceController:
    def __init__(self, ip_address, port, timeout, password):
        if not isinstance(ip_address, str):
            raise ValueError("Invalid IP address")
        if not isinstance(port, int):
            raise ValueError("Invalid port")
        if not isinstance(timeout, int):
            raise ValueError("Invalid timeout")
        self.connection = None
        self.ip_address = ip_address
        self.port = port
        self.timeout = timeout
        self.password = password
        self.zk = ZK(self.ip_address, self.port,self.timeout, self.password, force_udp=False, ommit_ping=False)


    def connect_to_device(self):
        try:
            # connect to device
            self.connection = self.zk.connect()
            return self.connection
        except (Exception) as e:
            logging.error(f"Process terminate for device {self.ip_address}:{self.port} : %s", e)
            raise ValueError("Failed to connect to device")
    def disable_device(self):
        if self.connection:
            self.connection.disable_device()
        else:
            raise ValueError("Invalid Connection")

    # Function to disconnect from the fingerprint device
    def disconnect_from_device(self):
         if self.connection:
            self.connection.disconnect()
         else:
            raise ValueError("Invalid Connection")
        
if __name__ == "__main__":
    # Instantiate DeviceConnection with your device's IP, port, timeout, and password
    # Should come from the interface
    device = ZKDeviceController(ip_address='192.168.1.222', port=4370, timeout=5, password=0)

    try:
        # Connect to the device
        connection = device.connect_to_device()
        print(connection)
        device.zk.test_voice()
        # Disable the device
        device.disable_device()
        print("Device disabled!")
    except ValueError as e:
        logging.error(f"Error: {e}")
    finally:
        # Disconnect from the device
        device.disconnect_from_device()