from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.http import HttpRequest, JsonResponse, HttpResponseNotAllowed
from django.shortcuts import redirect
from django.shortcuts import render

from kritika_main.custom_auth_form import CustomAuthForm
from kritika_main.edit_form import EditForm
from kritika_main.models import KritikaUser
from kritika_main.models import Post, Topic
from kritika_main.models import Role


def get_posts_by_topic(topic_name: str):
    topic_id = Topic.objects.only("id").get(topic_name=topic_name).id
    return Post.objects.filter(topic=topic_id)


def home(request: HttpRequest):
    template_name = "homev2.html"
    posts = Post.objects.filter(status="Published", is_main=False)
    try:
        main_post = Post.objects.filter(is_main=True)[0]
    except:
        main_post = None
    form = CustomAuthForm()

    return render(
        request, template_name, {"posts": posts, "main_post": main_post, "form": form}
    )


def user_account(request: HttpRequest):
    if request.user is None:
        return redirect("/")
    else:
        user_from_db = KritikaUser.objects.get(pk=request.user.pk)
        return render(request, "user_account.html", {"user": user_from_db})


def kritika_admin(request: HttpRequest):
    template_name = "kritika_admin.html"
    if request.user is None:
        return redirect("/")
    else:
        user_from_db = KritikaUser.objects.get(
            pk=request.user.pk
        )
        if user_from_db.role == str(Role.CLIENT):
            editable_posts = []
            return render(request, template_name, {"posts": editable_posts})
        elif user_from_db.role == str(Role.AUTHOR):
            editable_posts = Post.objects.filter(user=request.user.pk)
            return render(request, template_name, {"posts": editable_posts})
        elif user_from_db.role == str(Role.ADMIN):
            editable_posts = Post.objects.all()
            return render(request, template_name, {"posts": editable_posts})


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


def games_topic(request: HttpRequest):
    posts = get_posts_by_topic("Игры")
    return render(request, "books.html", {"posts": posts})


def exhibitions_topic(request: HttpRequest):
    posts = get_posts_by_topic("Выставки")
    return render(request, "books.html", {"posts": posts})


def login_user(request: HttpRequest):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, email=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("/")
    else:
        return redirect("/")


def editor(request: HttpRequest, article_id: int):
    post = Post.objects.select_related("user").get(pk=article_id)
    form = EditForm(instance=post)
    return render(request, "editor.html", {"post": post, "form": form})


def edit_post(request: HttpRequest):
    post = Post.objects.select_related("user").get(pk=request.POST.get("pk"))
    form = EditForm(request.POST, instance=post)
    if form.is_valid():
        print("Post form is valid")
        form.save()
        return render(request, "editor.html", {"form": form, "post": post})
    else:
        print("Post form is invalid")
        return redirect("/kritika_admin/")


def logout_user(request: HttpRequest):
    logout(request)
    return redirect("/")


def manifest(request: HttpRequest):
    return render(request, "manifest.html", {})


def search(request: HttpRequest):
    return render(request, "search.html", {})


def is_not_empty(string: str):
    return string is not None and len(string) > 0


def search_query(request: HttpRequest):
    if request.GET:
        search_results = []
        search_query_string = request.GET["query"]
        page = request.GET.get('page', 1)
        if is_not_empty(search_query_string):
            searched_posts = Post.objects.filter(heading__icontains=search_query_string).order_by("heading")
            page = Paginator(searched_posts, 10).page(page)
            search_results = list(map(lambda post: post.to_json(), page))
        return JsonResponse(data={"search_results": search_results})
    else:
        return HttpResponseNotAllowed(['GET'])
