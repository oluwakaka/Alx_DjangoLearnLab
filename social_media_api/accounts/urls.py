from django.urls import path
from .views import RegisterView, LoginView, ProfileView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    follow_user,
    unfollow_user,
    FollowingListView,
    FollowersListView,
)

urlpatterns = [
    # Authentication
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),

    # Profile
    path("profile/", ProfileView.as_view(), name="profile"),

    # Follow system
    path("follow/<int:user_id>/", follow_user, name="follow-user"),
    path("unfollow/<int:user_id>/", unfollow_user, name="unfollow-user"),
    path("following/", FollowingListView.as_view(), name="following-list"),
    path("followers/", FollowersListView.as_view(), name="followers-list"),
]
