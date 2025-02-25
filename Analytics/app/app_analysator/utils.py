import os
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
import pandas as pd
import time

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
            start_time = time.time()
            print('Start',start_time)
            try:
                df = func_read[extension](uploaded_file)
                end_time = time.time()
                print('end_time',end_time)
                return df
            except Exception as e:
                raise ValueError(f"error processing file {uploaded_file}")
    

    @staticmethod        
    def get_allowed_formats():
        return ['.json', '.csv', '.xls', '.xlsx']


class DataProcesor:
    """Сlass is responsible for data processing"""

    @staticmethod
    def add_emty_values_columns(df):
        """Adds a column with a count of empty values."""
        df['empty values'] = df.isnull().sum(axis=1)
        return df
    
    @staticmethod
    def get_data_shape(df):
        """Returns the number of rows and columns."""
        return df.shape


class AuthenticatedView(View):
    reverse_url = 'users:login'

    """Base class for views that require user authentication checks.
    Attributes:
    reverse_url (str): URL to redirect unauthenticated users to.
    Defaults to login page ('users:login')
    Methods:
    dispatch: Checks if user is authenticated. If not, redirects to URL
    specified in `reverse_url`. Otherwise, continue executing request"""


    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse(self.reverse_url))
        return super().dispatch(request, *args, **kwargs)
    
