"""THis module defines the video_app endpoints."""
from django.urls import path
from video_app.views import UploadFile, CompletedUpload, StreamVideo


urlpatterns = [
    path('api/chunked-upload/', UploadFile.as_view(), name='chunked-upload'),
    path('api/chunked-upload', UploadFile.as_view(), name='chunked-upload'),
    path('api/completed-upload/', CompletedUpload.as_view(), name='completed-upload'),
    path('api/completed-upload', CompletedUpload.as_view(), name='completed-upload'),
    path('api/videos/<str:video_id>/', StreamVideo.as_view(), name='get-video-chunk'),
    path('api/videos/<str:video_id>', StreamVideo.as_view(), name='get-video-chunk'),
]
