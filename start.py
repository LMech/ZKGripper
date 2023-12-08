from modules.zk_interaction_utils import ZKDeviceController
from modules.data_converter import DataConverter

def start_data_conversion():
    # Initialize the ZKDeviceController
    device_controller = ZKDeviceController(ip_address='192.168.1.222', port=4370, timeout=5, password="0")
    device_controller.create_zk_instance()

    try:
        # Connect to the device
        device_controller.connect_to_device()

        # Retrieve  data
        attendance_data = device_controller.retrieve_attendance_data()
        users_data = device_controller.retrieve_users_data()

        if attendance_data:
            # Create DataConverter instance
            converter = DataConverter(file_format='excel')

            # Convert data to Excel file
            converter.convert_att_to_file(attendance_data)
            converter.convert_users_to_file(users_data)
        else:
            print("No attendance data retrieved.")
    except ValueError as e:
        print(f"Error: {e}")
    finally:
        # Disconnect from the device
        device_controller.disconnect_from_device()

if __name__ == "__main__":
    start_data_conversion()