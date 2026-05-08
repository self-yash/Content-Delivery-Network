from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ImageModel,Service
import uuid

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