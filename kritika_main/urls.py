from django.contrib import admin
from django.urls import path, include
from kritika_main import views

urlpatterns = [
    path("articles/<int:article_id>/", views.article, name="main-view"),
    path("books/", views.books_topic, name="books_topic"),
    path("music/", views.music_topic, name="music_topic"),
    path("cinema/", views.cinema_topic, name="cinema_topic"),
    path("theatre/", views.theatre_topic, name="theatre_topic"),
]
