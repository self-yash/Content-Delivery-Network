from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Image,Service

import uuid
import os

CDN_DOMAIN = "https://cdn.nexiotech.cloud"

UPLOAD_DIR = "/var/www/images"


@api_view(['POST'])
def register_service(request):

    name = request.data.get('name')

    if not name:
        return Response({
            "error": "Service name is required"
        }, status=400)

    service = Service.objects.create(
        name=name,
        api_key=str(uuid.uuid4())
    )

    return Response({
        "message": "Service registered successfully",
        "service": {
            "id": service.id,
            "name": service.name,
            "api_key": service.api_key,
            "is_active": service.is_active,
            "created_at": service.created_at
        }
    })

@api_view(['POST'])
def upload_image(request):

    api_key = request.headers.get("X-API-KEY")

    if not api_key:
        return Response({
            "error": "API key required"
        }, status=401)

    try:
        service = Service.objects.get(
            api_key=api_key,
            is_active=True
        )

    except Service.DoesNotExist:
        return Response({
            "error": "Invalid API key"
        }, status=403)

    image = request.FILES.get("image")

    if not image:
        return Response({
            "error": "No image provided"
        }, status=400)

    # original filename
    original_name = image.name

    # extension
    ext = original_name.split('.')[-1]

    # generate UUID filename
    stored_name = f"{uuid.uuid4()}.{ext}"

    # final path
    save_path = os.path.join(
        UPLOAD_DIR,
        stored_name
    )

    # save file manually
    with open(save_path, 'wb+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)

    # save metadata in MySQL
    Image.objects.create(
        service=service,
        original_name=original_name,
        stored_name=stored_name,
        file_size=image.size,
        mime_type=image.content_type
    )

    image_url = f"{CDN_DOMAIN}/{stored_name}"

    return Response({
        "message": "Image uploaded successfully",
        "image_url": image_url
    })

@api_view(['POST'])
def regenerate_api_key(request):

    service_id = request.data.get("service_id")
    service_name = request.data.get("service_name")

    if not service_id or not service_name:
        return Response({
            "error": "service_id and service_name are required"
        }, status=400)

    try:
        service = Service.objects.get(
            id=service_id,
            name=service_name
        )

    except Service.DoesNotExist:
        return Response({
            "error": "Service not found"
        }, status=404)

    # generate new API key
    new_api_key = str(uuid.uuid4())

    # replace old key
    service.api_key = new_api_key
    service.save()

    return Response({
        "message": "API key regenerated successfully",
        "service": {
            "id": service.id,
            "name": service.name,
            "new_api_key": service.api_key
        }
    })