from django.urls import path
from .views import search_view, download, fetch_next_video_info, DownloadVideoView

urlpatterns = [
    path('search/', search_view, name='search'),
    path('download/', download, name='download'),
    path('next/', fetch_next_video_info, name='next'),
    path('download-video/', DownloadVideoView.as_view(), name='download_video')


]
