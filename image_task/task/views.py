from urllib.request import Request
from task.models import User as UserProfile, Image
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from .utils import resize_image, check_unique_name, check_resolution
import imghdr


@api_view(["POST"])
def post_image(request: Request) -> Response:
    if request.method == "POST":
        image = request.FILES["file"]
        extension = imghdr.what(image)
        if not check_unique_name(request.data["name"], Image):
            return Response(
                "Image name is already in our database. Please change image name."
            )
        elif extension in ["jpg", "png"]:
            owner = User.objects.get(id=request.data["owner_id"])
            name = request.data["name"]
            Image.objects.create(owner=owner.user, name=name, image=image)
            image = Image.objects.get(name=name)
            if owner.user.tier in ["Premium", "Enterprise"]:
                resize_image(image, (400, 400), name)
                resize_image(image, (200, 200), name)
                return Response(f"Image was uploaded for {owner.user.tier} user")
            else:
                resize_image(image, (200, 200), name)
                return Response("Image was uploaded for Basic user")
        else:
            return Response(
                "Invalid image extension. Please upload image in jpg/png format."
            )


@api_view(["POST"])
def get_image_by_owner(request: Request) -> Response:
    owner_name = request.data["name"]
    owner = UserProfile.objects.get(name=owner_name)
    images = Image.objects.filter(owner=owner)
    names = []
    for image in images:
        if owner.tier == "Basic":
            width, height = check_resolution(image.image)
            names.append(image.image.url) if width < 201 and height < 201 else None
        else:
            names.append(image.image.url)
    return Response(names)


@api_view(["POST"])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data["username"])
        user.set_password(request.data["password"])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)


@permission_classes((permissions.AllowAny))
@api_view(["POST"])
def login(request):
    user = get_object_or_404(User, username=request.data["username"])
    if not user.check_password(request.data["password"]):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    print(user)
    user = authenticate(
        request._request,
        username=request.data["username"],
        password=request.data["password"],
    )
    return Response({"token": token.key, "user": serializer.data})


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed!")
