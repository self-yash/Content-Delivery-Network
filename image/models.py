from django.db import models
import uuid

def upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return f"{uuid.uuid4()}.{ext}"

class ImageModel(models.Model):
    image = models.ImageField(upload_to=upload_path)