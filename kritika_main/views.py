from django.shortcuts import render
from django.http import HttpRequest
from kritika_main.models import Post, Topic

# Create your views here.


def get_posts_by_topic(topic_name: str):
    topic_id = Topic.objects.only("id").get(topic_name=topic_name).id
    return Post.objects.filter(topic=topic_id)


def home(request: HttpRequest):
    template_name = "home.html"
    posts = Post.objects.filter(status="Published")

    return render(request, template_name, {"posts": posts})


def article(request: HttpRequest, article_id: int):
    post = Post.objects.select_related("user").get(pk=article_id)
    return render(request, "article.html", {"post": post})


def books_topic(request: HttpRequest):
    posts = get_posts_by_topic("Книги")
    return render(request, "books.html", {"posts": posts})


def music_topic(request: HttpRequest):
    posts = get_posts_by_topic("Музыка")
    return render(request, "books.html", {"posts": posts})


def cinema_topic(request: HttpRequest):
    posts = get_posts_by_topic("Кино")
    return render(request, "books.html", {"posts": posts})


def theatre_topic(request: HttpRequest):
    posts = get_posts_by_topic("Театр")
    return render(request, "books.html", {"posts": posts})
