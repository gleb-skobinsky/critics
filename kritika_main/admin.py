from django.contrib import admin

from .models import KritikaUser, Topic, Post, PostImage


# Register your models here.


class TopicAdmin(admin.ModelAdmin):
    list_display = ["topic_name"]


class RoleAdmin(admin.ModelAdmin):
    list_display = ["role_name"]


class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "phone", "is_staff", "is_active", "role"]


class PostAdmin(admin.ModelAdmin):
    list_display = [
        "heading",
        "summary",
        "cover_image",
        "user",
        "topic",
    ]


class PostImageAdmin(admin.ModelAdmin):
    list_display = ["image", "image_caption"]


admin.site.register(Topic, TopicAdmin)
admin.site.register(KritikaUser, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostImage, PostImageAdmin)
