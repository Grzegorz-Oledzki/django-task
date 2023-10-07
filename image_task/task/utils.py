from PIL import Image as Pil
from .models import Image
from django.core.files.base import ContentFile
from django.db import models
import os


def resize_image(image: Image, size: tuple[int, int], name: str) -> None:
    picture_copy = ContentFile(image.image.read())
    extension = os.path.splitext(image.image.name)[-1]
    new_picture_name = f"{name}_{size[1]}px"
    is_unique_name: bool = check_unique_name(new_picture_name, Image)
    if not is_unique_name:
        new_picture_name = make_name_unique(new_picture_name, False)
    image.pk = None
    image.original_image = False
    image.name = new_picture_name
    image.image.save(f"{new_picture_name}{extension}", picture_copy)
    picture_copy = Pil.open(image.image.path)
    picture_copy.thumbnail(size, Pil.LANCZOS)
    picture_copy.save(image.image.path)


def check_unique_name(name: str, model: models.Model) -> bool:
    for item in model.objects.all():
        if str(item.name).lower() == name.lower():
            return False
    return True


def check_resolution(image: models.ImageField):
    return Pil.open(image).size


def make_name_unique(not_unique_name: str, is_unique_name: bool) -> str:
    i = 1
    while not is_unique_name:
        new_picture_name = f"{not_unique_name}_{i}"
        is_unique_name: bool = check_unique_name(new_picture_name, Image)
        i += 1
    return new_picture_name
