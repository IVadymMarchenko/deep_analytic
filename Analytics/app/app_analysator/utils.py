import os
import pandas as pd


class FileAssistant:

    @staticmethod
    def get_file_extencion(file_name):
        extension = os.path.splitext(file_name)[1].lower()
        return extension


    @staticmethod
    def read_file(uploaded_file):
        extension = FileAssistant.get_file_extencion(uploaded_file.name).lower()
        func_read = {
                    ".csv": pd.read_csv,
                    ".json": pd.read_json,
                    ".xlsx": pd.read_excel,
                     ".xls": pd.read_excel
                     }
        if extension in func_read:
            try:
                df = func_read[extension](uploaded_file)
                return df
            except Exception as e:
                raise ValueError(f"error processing file {uploaded_file}")
    

    @staticmethod        
    def get_allowed_formats():
        return ['.json', '.csv', '.xls', '.xlsx']

