from django.urls import path,include
from .views import (FileUploadAPI,ListFileUploadAPI,ListRecievedFileAPI,)
urlpatterns = [
    path("upload_transfer_file/",FileUploadAPI.as_view(),name="file-upload-transfer"),
    path("list_file_uploads/",ListFileUploadAPI.as_view(),name="list-file-uploads"),
    path("list_recieved_files/",ListRecievedFileAPI.as_view(),name="list-recieved-files"),
]

