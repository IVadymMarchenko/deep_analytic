from django.urls import path
from .import views



app_name = 'display_data'


urlpatterns = [
     path("data-on-the-graph/",views.ViewData.as_view(),name="view_data"),
]