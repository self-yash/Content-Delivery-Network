from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient
from .models import ImageModel

client = MongoClient("mongodb://root:yourStrongPassword@localhost:27017/admin")
db = client["image_db"]
collection = db["images"]

CDN_DOMAIN = "https://cdn.nexiotech.cloud"

@api_view(['POST'])
def upload_image(request):
    image = request.FILES.get('image')

    if not image:
        return Response({"error": "No image provided"}, status=400)

    obj = ImageModel.objects.create(image=image)

    # build CDN URL
    image_url = {obj.image.url}

    # store in MongoDB
    collection.insert_one({
        "image_url": image_url
    })

    return Response({
        "message": "Uploaded",
        "url": image_url
    })