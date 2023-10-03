from rest_framework import serializers
from django.contrib.auth.models import User
from task.models import Image


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ["id", "username", "password", "email"]


class ImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        image = Image.objects.create(**validated_data)
        return image

    class Meta:
        model = Image
        fields = ["name"]
