import uuid
from typing import List
from django.db import models
from django.contrib.auth.models import User as DjangoUser


class User(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    user = models.OneToOneField(
        DjangoUser, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=50, blank=True, null=True)
    tier = models.ForeignKey("Tier", on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self) -> str:
        return str(self.name)


class Image(models.Model):
    image = models.ImageField(null=True, blank=False, upload_to="images/")
    name = models.CharField(max_length=50, blank=True, null=True, unique=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    original_image = models.BooleanField(default=False)


class Tier(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    thumbnail_height_1 = models.IntegerField(blank=False, null=False, unique=False)
    thumbnail_height_2 = models.IntegerField(blank=True, null=True, unique=False)
    thumbnail_height_3 = models.IntegerField(blank=True, null=True, unique=False)
    thumbnail_height_4 = models.IntegerField(blank=True, null=True, unique=False)
    orginal_link = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    def all_thumbnail_height(self) -> List[int]:
        sizes = [
            self.thumbnail_height_1,
            self.thumbnail_height_2,
            self.thumbnail_height_3,
            self.thumbnail_height_4,
        ]
        return [size for size in sizes if size]
