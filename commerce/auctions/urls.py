from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("details/<int:id>", views.listing_details, name="details"),
    path("closed/<int:id>", views.close_bid, name="closed"),
    path("add-to-watchlist/<int:id>", views.add_to_watchlist, name="add-to-watchlist"),
    path("remove-from-watchlist/<int:id>", views.remove_from_watchlist, name="remove-from-watchlist"),
    path("watchlist", views.watchlist, name="watchlist")
]
