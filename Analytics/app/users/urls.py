from django.urls import path
from django.views.decorators.cache import cache_page
from . import views



app_name = 'users'


urlpatterns = [
     path("",  views.BaseView.as_view(), name="users"),
     path("login/",  views.UserLoginView.as_view(), name="login"),
     path("registration/",  views.UserRegistrationView.as_view(), name="registration"),
     path("logout/",  views.logout, name="logout"),  
]