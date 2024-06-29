from django.urls import path
from .views import (
    UserSignupView,
    UserLoginAPIView,
    UserSearchView,
    SendFriendRequestView,
    AcceptFriendRequestView,
    RejectFriendRequestView,
    ListAcceptFriendRequestView,
    ListPendingFriendRequestView,
)

urlpatterns = [
    path("register/", UserSignupView.as_view(), name="register"),
    path("login/", UserLoginAPIView.as_view(), name="login"),
    path("search/", UserSearchView.as_view(), name="user-search"),
    path(
        "send_friend_request/",
        SendFriendRequestView.as_view(),
        name="send-friend-request",
    ),
    path(
        "accept_friend_request/<int:pk>",
        AcceptFriendRequestView.as_view(),
        name="accept-friend-request",
    ),
    path(
        "reject_friend_request/<int:pk>",
        RejectFriendRequestView.as_view(),
        name="reject-friend-request",
    ),
    path(
        "list_accepted_friend_request/",
        ListAcceptFriendRequestView.as_view(),
        name="send-friend-request",
    ),
    path(
        "list_pending_friend_request/",
        ListPendingFriendRequestView.as_view(),
        name="send-friend-request",
    ),
]
