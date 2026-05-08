from django.urls import path
from .views import register_service, upload_image

app_name = 'image'

urlpatterns = [
    path('register/', register_service),
]