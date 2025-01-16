from django import forms
from .models import MyFile
from .utils import FileAssistant
import os


class MyFileForm(forms.ModelForm):
    class Meta:
        model = MyFile
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data.get('file')  # Получаем файл из cleaned_data
        if file:
            # Проверка на размер файла
            max_size = 20 * 1024 * 1024  # 5 MB
            if file.size > max_size:
                raise forms.ValidationError("The file is too large. Maximum file size is 5 MB.")

            allowed_formats = FileAssistant.get_allowed_formats()
            ext =  FileAssistant.get_file_extencion(file.name)  # Получаем расширение файла
            if ext.lower() not in allowed_formats:
                raise forms.ValidationError(f"Invalid file format. Only allowed: {', '.join(allowed_formats)}.")
        
        return file