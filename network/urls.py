from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:user_id>", views.user_info, name="user_info"),
    path("handle_follow", views.handle_follow, name="handle_follow"),
    path("handle_unfollow", views.handle_unfollow, name="handle_unfollow"),
    path("display_following", views.display_following, name="display_following"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("add_like/<int:post_id>", views.add_like, name="add_like"),
    path("delete_like/<int:post_id>", views.delete_like, name="delete_like")
]
