from django.urls import path

from .views import CreateUserView, CreateFriendshipRequestView, ProcessFriendshipRequestView, \
    GetFriendshipRequestsView, GetFriendshipStatusView, GetUserFriendsView, RemoveFromFriendsView

urlpatterns = [
    path("create_user/", CreateUserView, name="create_user"),
    path("create_friendship_request/", CreateFriendshipRequestView, name="create_friendship_request"),
    path("process_friendship_request/", ProcessFriendshipRequestView, name="process_friendship_request"),
    path("get_user_friends/", GetUserFriendsView, name="get_user_view"),
    path("get_friendship_requests/", GetFriendshipRequestsView, name="get_friendship_requests"),
    path("get_friendship_status/", GetFriendshipStatusView, name="get_friendship_status"),
    path("remove_from_friends/", RemoveFromFriendsView, name="remove_from_friends")
]
