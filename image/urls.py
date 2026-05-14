from django.urls import path
from .views import *

app_name = 'image'

urlpatterns = [
    path('register/', register_service),
    path('upload/', upload_image),
    path('regenerate-key/', regenerate_api_key),
]