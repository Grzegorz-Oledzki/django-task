import imghdr

from urllib.request import Request
from task.models import Image
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from task.utils import resize_image, check_unique_name, make_name_unique
from task.serializers import ImageSerializer
from django.core.exceptions import ValidationError, ObjectDoesNotExist


@api_view(["POST"])
def post_image(request: Request) -> Response:
    if request.method == "POST":
        try:
            owner = User.objects.get(id=request.data["owner_id"])
        except (ValidationError, ObjectDoesNotExist):
            return Response("Cannot find user. Please check correctness of user id")
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
            if not tier:
                return Response(
                    f"User does not have tier. Please add tier for {owner.user} user."
                )
            for size in tier.all_thumbnail_height():
                resize_image(image, (size, size), name)
            return Response(
                f"Image was uploaded for {owner.user} user with tier {owner.user.tier}"
            )
        else:
            return Response(
                f"Wrong image format, accepted formats: 'jpeg', 'jpg', 'png'"
            )


@api_view(["POST"])
def get_image_by_owner(request: Request) -> Response:
    if request.method == "POST":
        try:
            owner = User.objects.get(id=request.data["owner_id"])
        except (ValidationError, ObjectDoesNotExist):
            return Response("Cannot find user. Please check correctness of user id")
        print(owner)
        images = Image.objects.filter(owner=owner.user)
        tier = owner.user.tier
        if not tier:
            return Response(
                f"User does not have tier. Please add tier for {owner.user} user."
            )
        images_links = [
            image.image.url
            for image in images
            if not image.original_image or tier.orginal_link and image.original_image
        ]
        return Response(
            images_links if images_links else "User does not have any images"
        )
