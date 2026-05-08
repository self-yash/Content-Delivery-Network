from django.db import models
import uuid
import os 

def generate_filename(filename):
    ext = filename.split('.')[-1]
    return f"{uuid.uuid4()}.{ext}"

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

class Image(models.Model):

    id = models.AutoField(primary_key=True)

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE
    )

    original_name = models.CharField(max_length=255)

    stored_name = models.CharField(
        max_length=255,
        unique=True
    )

    file_size = models.IntegerField(null=True)

    mime_type = models.CharField(
        max_length=50,
        null=True
    )

    image = models.ImageField(
        upload_to='',
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "images"