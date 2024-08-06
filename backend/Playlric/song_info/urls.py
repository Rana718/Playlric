from django.urls import path
from .views import search, download

urlpatterns = [
    path('search/', search, name='search'),
    path('download/', download, name='download'),
]
