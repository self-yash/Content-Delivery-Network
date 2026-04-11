from django.urls import path
from .views import upload_image

app_name = 'image'

urlpatterns = [
    path('upload/', upload_image),
]