from django.contrib import admin
from django.urls import path, include
from kritika_main import views

urlpatterns = [
    path("articles/<int:article_id>/", views.article, name="article"),
    path("books/", views.books_topic, name="books_topic"),
    path("music/", views.music_topic, name="music_topic"),
    path("cinema/", views.cinema_topic, name="cinema_topic"),
    path("interviews/", views.interviews_topic, name="interviews_topic"),
    path("games/", views.games_topic, name="games_topic"),
    path("exhibitions/", views.exhibitions_topic, name="exhibitions_topic"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("user_account/", views.user_account, name="user_account"),
    path("kritika_admin/", views.kritika_admin, name="kritika_admin"),
    path("editor/<int:article_id>/", views.editor, name="editor"),
    path("edit_post/", views.edit_post, name="edit_post"),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("oauth/", include("social_django.urls", namespace="social")),
    path("manifest/", views.manifest, name="manifest"),
    path("search/", views.search, name="search"),
    path("search-query/", views.search_query, name="search-query")
]
