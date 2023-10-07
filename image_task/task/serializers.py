from rest_framework import serializers
from django.contrib.auth.models import User
from task.models import Image


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ["id", "username", "password", "email"]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            "image",
            "name",
        ]
        read_only_fields = ["owner_id"]
