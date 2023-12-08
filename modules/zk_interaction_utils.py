from zk import ZK, const
import logging
import hashlib
import re

class ZKDeviceController:
    def __init__(self, ip_address: str, port: int, timeout: int, password: str):
        if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip_address):
            raise ValueError("Invalid IP address format")
        if not isinstance(port, int):
            raise ValueError("Invalid port")
        if not isinstance(timeout, int):
            raise ValueError("Invalid timeout")
        self.connection = None
        self.ip_address = ip_address
        self.port = port
        self.timeout = timeout
        self.password = self.password = hashlib.sha256(password.encode()).hexdigest()
        self.zk = None
    def create_zk_instance(self):
        try:
            self.zk = ZK(self.ip_address, self.port,self.timeout, self.password, force_udp=False, ommit_ping=False)
        except Exception as e:
            logging.error(f"Failed to initialize ZK: {e}")
            raise ValueError("Failed to initialize ZK")

    def connect_to_device(self):
        try:
            # connect to device
            self.connection = self.zk.connect()
            self.connection.read_sizes()
            return self.connection
        except (Exception) as e:
            logging.error(f"Process terminate for device {self.ip_address}:{self.port} : %s", e)
            raise ValueError("Failed to connect to device")
    def disable_device(self):
        if self.connection:
            self.connection.disable_device()
        else:
            raise ValueError("Invalid Connection")
        
    def enable_device(self):
        if self.connection:
            self.connection.enable_device()
        else:
            raise ValueError("Invalid Connection")

    # Function to disconnect from the fingerprint device
    def disconnect_from_device(self):
         try:
            self.connection.disconnect()
            self.connection = None
         except:
            raise ValueError("Invalid Connection")
        
    def retrieve_attendance_data(self):
        try:
            if self.connection:
                attendances = self.connection.get_attendance()
                if len(attendances) == 0:
                    logging.warning("No attendance data found")
                return attendances
            else:
                logging.warning("Invalid Connection")
                return None
        except Exception as e:
            logging.error(f"Error retrieving attendance data: {e}")
            return None
        
# if __name__ == "__main__":
#     # Instantiate DeviceConnection with your device's IP, port, timeout, and password
#     # Should come from the interface
#     device = ZKDeviceController(ip_address='192.168.1.222', port=4370, timeout=5, password="0")
#     device.create_zk_instance()

#     try:
#         # Connect to the device
#         connection = device.connect_to_device()
#         print(connection)
#         device.disable_device()
#         print("Device disabled!")
#         device.enable_device()
#     except ValueError as e:
#         logging.error(f"Error: {e}")
#     finally:
        # Disconnect from the device
        device.disconnect_from_device()