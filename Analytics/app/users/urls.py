from django.urls import path
from django.views.decorators.cache import cache_page
from . import views



app_name = 'users'


urlpatterns = [
     path("",  views.base, name="users"),
     path("login/",  views.login, name="login"),
     path("registration/",  views.registration, name="registration"),
     path("logout/",  views.logout, name="logout"),  
]