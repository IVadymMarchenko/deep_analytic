from django.urls import path
from . import views



app_name = 'profile'


urlpatterns = [
     path('<str:username>/<int:user_id>/', views.UserProfileView.as_view(), name='profile'),   
]