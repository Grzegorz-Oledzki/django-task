from django.contrib import admin

from task.models import User, Image


@admin.register(User)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "tier")


@admin.register(Image)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name"]
