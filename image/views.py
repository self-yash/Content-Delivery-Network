from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Image,Service
import uuid
import os

CDN_DOMAIN = "https://cdn.nexiotech.cloud"

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

    # generate unique filename
    ext = image.name.split('.')[-1]
    stored_name = f"{uuid.uuid4()}.{ext}"

    obj = Image.objects.create(
        service=service,

        original_name=image.name,

        stored_name=stored_name,

        file_size=image.size,

        mime_type=image.content_type,

        image=image
    )

    # rename actual stored file
    old_path = obj.image.path

    new_path = os.path.join(
        os.path.dirname(old_path),
        stored_name
    )

    os.rename(old_path, new_path)

    obj.image.name = stored_name
    obj.save()

    return Response({
        "message": "Image uploaded successfully",
        "image_url": obj.image.url
    })