from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
import json
from modules.data_converter import DataConverter
from modules.zk_interaction_utils import ZKDeviceController


class ZKGInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.device_controller = None
        self.device_enabled = False

    def init_ui(self):
        layout = QVBoxLayout()

        self.title_label = QLabel('Attendance System')
        layout.addWidget(self.title_label)

        self.btn_connect = QPushButton('Connect')
        self.btn_connect.clicked.connect(self.toggle_connection)
        layout.addWidget(self.btn_connect)

        self.btn_device = QPushButton('Enable Device')
        self.btn_device.clicked.connect(self.toggle_device)
        self.btn_device.setEnabled(False)  # Initially disabled
        layout.addWidget(self.btn_device)

        self.btn_export_users = QPushButton('Export Users Data')
        self.btn_export_users.clicked.connect(self.export_users_data)
        self.btn_export_users.setEnabled(False)  # Initially disabled
        layout.addWidget(self.btn_export_users)

        self.btn_export_attendance = QPushButton('Export Attendance Data')
        self.btn_export_attendance.clicked.connect(self.export_attendance_data)
        self.btn_export_attendance.setEnabled(False)  # Initially disabled
        layout.addWidget(self.btn_export_attendance)

        self.setLayout(layout)
        self.setWindowTitle('Attendance System')

    def toggle_connection(self):
        if not self.device_controller:
            self.connect_to_device()
        else:
            self.disconnect_from_device()

    def connect_to_device(self):
        settings = read_settings()
        try:
            if self.device_controller:
                # If already connected, disconnect first
                self.disconnect_from_device()
            
            # Connect to the device
            self.device_controller = ZKDeviceController(ip_address=settings['device_settings']['ip_address'],
                                                        port=settings['device_settings']['port'],
                                                        timeout=settings['device_settings']['timeout'],
                                                        password=settings['device_settings']['password'])
            self.device_controller.create_zk_instance()
            self.device_controller.connect_to_device()
            self.btn_connect.setText('Disconnect')
            self.btn_device.setEnabled(True)
            self.btn_export_users.setEnabled(True)
        except ValueError as e:
            self.show_error_dialog(f"Error connecting to device: {e}")

    def disconnect_from_device(self):
        try:
            if self.device_controller:
                # Disconnect from the device
                self.device_controller.disconnect_from_device()
                self.device_controller = None
                self.btn_connect.setText('Connect to Device')
                self.btn_device.setEnabled(False)
                self.btn_export_users.setEnabled(False)
        except ValueError as e:
            self.show_error_dialog(f"Error disconnecting from device: {e}")

    def toggle_device(self):
        if self.device_controller:
            try:
                if self.device_enabled:
                    self.device_controller.disable_device()
                    print("Device disabled")
                    self.device_enabled = False
                    self.btn_device.setText('Enable Device')
                else:
                    self.device_controller.enable_device()
                    print("Device enabled")
                    self.device_enabled = True
                    self.btn_device.setText('Disable Device')
            except ValueError as e:
                self.show_error_dialog(f"Error toggling device: {e}")
        else:
            print("Please connect to the device first")

    def export_users_data(self):
        try:
            users_data = self.device_controller.retrieve_users_data()
            if users_data:
                converter = DataConverter(file_format='excel')
                converter.convert_users_to_file(users_data)
            else: 
                print("No users data retrieved.")
        except ValueError as e:
            self.show_error_dialog(f"Error exporting users data: {e}")
             
    def export_attendance_data(self):
        try:
            attendance_data = self.device_controller.retrieve_attendance_data()
            if attendance_data:
                converter = DataConverter(file_format='excel')
                converter.convert_att_to_file(attendance_data)
            else: 
                print("No attendance data retrieved.")
        except ValueError as e:
            self.show_error_dialog(f"Error exporting attendance data: {e}")

    def show_error_dialog(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(message)
        msg.setWindowTitle("Error")
        msg.exec_()

def read_settings():
    # Read settings from JSON file
    with open('settings.json', 'r') as file:
        settings = json.load(file)
    return settings 
