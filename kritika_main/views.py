from typing import List

from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponseNotAllowed, JsonResponse
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
    posts = Post.objects.filter(status="Published", is_main=False).order_by('-updated_at').distinct()[:4]
    try:
        main_post = Post.objects.filter(is_main=True)[0]
    except:
        main_post = None
    form = CustomAuthForm()

    return render(
        request=request, template_name="homev2.html", context={"posts": posts, "main_post": main_post, "form": form}
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
    results = results_for_page(request)
    if results.redirection:
        return redirect(f"/search/?query={results.query}&page={results.num_pages}")
    return render(
        request=request,
        template_name="search.html",
        context={
            "search_results": results.search_results,
            "num_pages": results.num_pages,
            "query": results.query,
            "current_page": str(results.current_page),
            "pagination_view": results.pagination_view
        }
    )


def is_not_empty(string: str):
    return string is not None and len(string) > 0


def chunk_array(array, chunk_size):
    return [array[i:i + chunk_size] for i in range(0, len(array), chunk_size)]


class SearchResults:
    def __init__(self, query: str,
                 search_results: List[List[dict]] = None,
                 num_pages: int = 1,
                 current_page: int = 1,
                 redirection: bool = False,
                 pagination_view: List[str] = None
                 ):
        self.query = query
        self.search_results = search_results
        self.num_pages = num_pages
        self.current_page = current_page
        self.redirection = redirection
        self.pagination_view = pagination_view

    def __str__(self):
        return f"SearchResults(query='{self.query}', search_results={self.search_results}, " \
               f"num_pages={self.num_pages}, current_page={self.current_page}, " \
               f"redirect={self.redirection}, pagination_view={self.pagination_view})"


def search_query(request: HttpRequest):
    if request.GET:
        results = results_for_page(request)
        return JsonResponse(data={"search_results": results.search_results, "num_pages": results.num_pages})
    else:
        return HttpResponseNotAllowed(['GET'])


def get_page(request: HttpRequest):
    page = request.GET.get("page", 1)
    try:
        page = int(page)
    except ValueError:
        page = 1
    page = page if page > 0 else 1
    return page


def results_for_page(request: HttpRequest) -> SearchResults:
    search_results = []
    num_pages = 1
    search_query_string = request.GET.get(key="query", default="")
    page_number = get_page(request)
    if is_not_empty(search_query_string):
        searched_posts = Post.objects.filter(heading__icontains=search_query_string).order_by("heading")
        paginator = Paginator(searched_posts, 9)
        num_pages = paginator.num_pages
        if page_number > num_pages:
            return SearchResults(
                query=search_query_string,
                current_page=page_number,
                num_pages=num_pages,
                redirection=True
            )
        page = paginator.page(page_number)
        search_results = list(map(lambda post: post.to_json(), page))
    return SearchResults(
        query=search_query_string,
        search_results=chunk_array(search_results, 3),
        num_pages=num_pages,
        current_page=page_number,
        pagination_view=construct_pages_list(page_number, num_pages)
    )


def construct_pages_list(current_page: int, total_pages: int) -> List[str]:
    if total_pages <= 5:
        return [str(i) for i in range(1, total_pages + 1)]
    elif current_page == 1 or current_page == total_pages:
        return ["1", "2", "...", str(total_pages - 1), str(total_pages)]
    elif 1 <= current_page <= 3:
        return [str(i) for i in range(1, 4)] + ["...", str(total_pages)]
    elif total_pages - 2 <= current_page <= total_pages:
        return ["1", "..."] + [str(i) for i in range(total_pages-2, total_pages+1)]
    else:
        return ["1", "...", str(current_page - 1), str(current_page), str(current_page + 1), "...", str(total_pages)]
