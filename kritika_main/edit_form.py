from django.forms import ModelForm
from kritika_main.models import Post
from django.forms import Textarea


class EditForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            "heading",
            "full_content",
            "status",
            "rating",
            "summary",
            "cover_image",
            "heading_image",
            "topic",
        ]
