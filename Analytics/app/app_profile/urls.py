from django.urls import path
from . import views



app_name = 'profile'


urlpatterns = [
    path("",  views.get_profile, name="prifile"),   
]