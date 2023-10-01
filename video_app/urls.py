"""THis module defines the video_app endpoints."""
# pylint: disable=unused-import
from django.urls import path
from video_app.views import UploadFile, CompletedUpload
from video_app.error_handler import custom_404_view


urlpatterns = [
    path('api/chunked-upload/', UploadFile.as_view(), name='chunked-upload'),
    path('api/chunked-upload', UploadFile.as_view(), name='chunked-upload'),
    path('api/completed-upload/', CompletedUpload.as_view(), name='completed-upload'),
    path('api/completed-upload', CompletedUpload.as_view(), name='completed-upload'),
]

# pylint: disable=invalid-name
handler404 = 'video_app.error_handler.custom_404_view'
