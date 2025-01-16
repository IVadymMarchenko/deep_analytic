from django.urls import path
from .import views



app_name = 'analysator'


urlpatterns = [
     path("upload-file/",  views.UploadFileView.as_view(), name="upload_file"), 
     path("upload-text-data/",  views.upload_text_data, name="upload_text"),
     path("table-data/",  views.TableView.as_view(), name="table"),
     path("make-graph/", views.MakeGraphsView.as_view(), name='make_graph')
]