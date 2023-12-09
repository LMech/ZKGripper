from datetime import datetime
import pandas as pd


class DataConverter:
    def __init__(self, file_format='excel'):
        self.file_format = file_format
    
    def convert_att_to_file(self, att_data):
        file_name = f"attendance_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        aslist = []
        for record in att_data:
            aslist.append((record.user_id, record.timestamp))
        if self.file_format == 'excel':
            file_name += ".xlsx" 
            self._convert_to_excel(aslist, file_name)
        # Add support for other formats here
        else:
            raise ValueError(f"Unsupported file format: {self.file_format}")

    def convert_users_to_file(self, users_data):
        file_name = f"users_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        aslist = []
        for record in users_data:
            aslist.append((record.user_id, record.name))
        if self.file_format == 'excel':
            file_name += ".xlsx" 
            self._convert_to_excel(aslist, file_name)
        # Add support for other formats here
        else:
            raise ValueError(f"Unsupported file format: {self.file_format}")
    def _convert_to_excel(self, aslist, file_name):
        df = pd.DataFrame(aslist)
        df.to_excel(file_name, index=False)
        