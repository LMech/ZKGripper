import json

from modules.zk_interaction_utils import ZKDeviceController
from modules.data_converter import DataConverter


def read_settings():
    # Read settings from JSON file
    with open('settings.json', 'r') as file:
        settings = json.load(file)
    return settings

def start_data_conversion():
    settings = read_settings()
    # Initialize the ZKDeviceController
    device_controller = ZKDeviceController(ip_address=settings['device_settings']['ip_address'],
                                           port=settings['device_settings']['port'],
                                           timeout=settings['device_settings']['timeout'],
                                           password=settings['device_settings']['password'])    
    device_controller.create_zk_instance()

    try:
        # Connect to the device
        device_controller.connect_to_device()

        # Retrieve  data
        attendance_data = device_controller.retrieve_attendance_data()
        users_data = device_controller.retrieve_users_data()

        if attendance_data:
            # Create DataConverter instance
            converter = DataConverter(file_format=settings['file_format'])

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