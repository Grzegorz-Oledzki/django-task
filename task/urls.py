from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from task import views

urlpatterns = [
    path("upload_image", views.post_image),
    path("get_image_by_owner", views.get_image_by_owner),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
