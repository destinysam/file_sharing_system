from django.urls import path
from .views import (SendMessageAPI,ListFileMessageAPI)


urlpatterns = [
    path("send_message/",SendMessageAPI.as_view(),name="send-message"),
    path("list_file_messages/<int:file_id>/",ListFileMessageAPI.as_view(),name="list-file-messages"),
]