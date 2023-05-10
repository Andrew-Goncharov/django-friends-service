from django.urls import path

from .views import create_user_view, create_friendship_request_view, process_friendship_request_view, \
    get_friendship_requests_view, get_friendship_status_view, get_user_friends_view, remove_from_friends_view

urlpatterns = [
    path("create_user/", create_user_view, name="create_user"),
    path("create_friendship_request/", create_friendship_request_view, name="create_friendship_request"),
    path("process_friendship_request/", process_friendship_request_view, name="process_friendship_request"),
    path("get_user_friends/", get_user_friends_view, name="get_user_view"),
    path("get_friendship_requests/", get_friendship_requests_view, name="get_friendship_requests"),
    path("get_friendship_status/", get_friendship_status_view, name="get_friendship_status"),
    path("remove_from_friends/", remove_from_friends_view, name="remove_from_friends")
]
