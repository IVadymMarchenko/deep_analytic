from django.urls import path
from .import views



app_name = 'download_char'


urlpatterns = [
     path("<int:char_id>",views.download,name="download_data"),
]