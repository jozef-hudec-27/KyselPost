from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("like-unlike/<str:pk>/", views.like_unlike, name="like_unlike"),
    path("create-post/", views.create_post, name="create_post"),
    path("logout/", views.logout_user, name="logout"),
    path("login/", views.login_page, name="login"),
    path("register/", views.register_user, name="register"),
    path("follow-unfollow/<str:pk>", views.follow_unfollow, name="follow_unfollow"),
    path("profile/<str:pk>/", views.profile, name="profile"),
    path("edit-user/", views.edit_user, name="edit"),
    path("users/", views.users, name="users"),
    path("followed-users/<str:pk>/", views.followed_users, name="followed_users"),
    path("following-users/<str:pk>/", views.following_users, name="following_users"),
]