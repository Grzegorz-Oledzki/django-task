from django.urls import path
from django.urls import re_path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from task import views

urlpatterns = [
    path("upload_image", views.post_image),
    path("get_image_by_owner", views.get_image_by_owner),
    re_path("signup", views.signup),
    re_path("login", views.login),
    re_path("test_token", views.test_token),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
