import imghdr

from urllib.request import Request
from task.models import User as UserProfile, Image
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .utils import resize_image, check_unique_name, make_name_unique
from task.serializers import ImageSerializer


@api_view(["POST"])
def post_image(request: Request) -> Response:
    if request.method == "POST":
        owner = User.objects.get(id=str(request.data["owner_id"]))
        request.data["owner_id"] = owner.id
        serializer = ImageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        image = request.FILES["file"]
        extension = imghdr.what(image)
        if not check_unique_name(request.data["name"], Image):
            request.data["name"] = make_name_unique(request.data["name"], False)
        if extension in ["jpeg", "jpg", "png"]:
            name = request.data["name"]
            Image.objects.create(
                owner=owner.user, name=name, image=image, original_image=True
            )
            image = Image.objects.get(name=name)
            tier = owner.user.tier
            for size in tier.all_thumbnail_height():
                resize_image(image, (size, size), name)
            return Response(f"Image was uploaded for user with tier {owner.user.tier}")
        else:
            return Response(
                f"Wrong image format, accepted formats: 'jpeg', 'jpg', 'png'"
            )


@api_view(["POST"])
def get_image_by_owner(request: Request) -> Response:
    owner_name = request.data["name"]
    owner = UserProfile.objects.get(name=owner_name)
    images = Image.objects.filter(owner=owner)
    names = [
        image.image.url
        for image in images
        if not image.original_image or owner.tier.orginal_link and image.original_image
    ]
    return Response(names)
