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
    
    def retrieve_users_data(self):
        try:
            if self.connection:
                users = self.connection.get_users()
                if len(users) == 0:
                    logging.warning("No users data found")
                return users
            else:
                logging.warning("Invalid Connection")
                return None
        except Exception as e:
            logging.error(f"Error retrieving users data: {e}")
            return None