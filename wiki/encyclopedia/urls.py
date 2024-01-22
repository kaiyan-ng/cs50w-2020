from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('<str:title>', views.entry, name="entry"),
    path("search/", views.search_results, name="search_results"),
    path("new_page/", views.new_page, name="create"),
    path("random/", views.random_page, name="random"),
    path("edit_page/<str:title>", views.edit_page, name="edit")
]
