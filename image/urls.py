from django.urls import path
from .views import register_service, upload_image

app_name = 'image'

urlpatterns = [
    path('upload/', upload_image),
    path('register/', register_service),
]