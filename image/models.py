from django.db import models
import uuid

def upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return f"{uuid.uuid4()}.{ext}"

class ImageModel(models.Model):
    image = models.ImageField(upload_to=upload_path)

class Service(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    api_key = models.CharField(
        max_length=255,
        unique=True,
        default=uuid.uuid4
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'services'