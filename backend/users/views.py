from django.shortcuts import render
from rest_framework import status

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import UserSerializer, FriendshipRequestSerializer, ProcessFriendshipRequestSerializer, \
    FriendSerializer
from .utils import user_exists, get_user_by_id, create_friendship_request, get_friendship_request, \
    accept_friendship_request, reject_friendship_request, is_valid_uuid, get_friendship_status, get_status, \
    get_user_friends, get_friends_list, get_sent_requests, get_received_requests, get_requests_list, \
    remove_from_friends, clear_friendship_requests, requests_from_both_users_exist, accept_both_requests


@api_view(["POST"])
def CreateUserView(request):
    if request.method == "POST":
        data = request.data
        serializer = UserSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_404_NOT_FOUND
            )

        serializer.save()
        return Response(
            data=serializer.errors,
            status=status.HTTP_201_CREATED
        )


@api_view(["POST"])
def CreateFriendshipRequestView(request):
    if request.method == "POST":
        data = request.data
        serializer = FriendshipRequestSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_404_NOT_FOUND
            )

        sender_id = serializer.data["sender"]
        receiver_id = serializer.data["receiver"]

        sender = get_user_by_id(sender_id)
        receiver = get_user_by_id(receiver_id)

        try:
            create_friendship_request(sender, receiver)
        except ValueError as e:
            return Response(
                data={"error message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        if requests_from_both_users_exist(sender, receiver):
            try:
                accept_both_requests(sender, receiver)
            except ValueError as e:
                pass
                # return Response(
                #     data={"error message": str(e)},
                #     status=status.HTTP_400_BAD_REQUEST
                # )

        return Response(
            data={"message": "FriendshipRequest successfully created"},
            status=status.HTTP_201_CREATED
        )



@api_view(["POST"])
def ProcessFriendshipRequestView(request):
    if request.method == "POST":
        data = request.data

        serializer = ProcessFriendshipRequestSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        sender = serializer.data["sender"]
        receiver = serializer.data["receiver"]
        action = serializer.data["action"]

        request = get_friendship_request(sender, receiver)

        if not request:
            return Response(
                data={"error message": "FriendshipRequest not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            if action == "accept":
                accept_friendship_request(request)

            if action == "reject":
                reject_friendship_request(request)

        except ValueError as e:
            return Response(
                data={"error message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )


@api_view(["GET"])
def GetFriendshipRequestsView(request):
    if request.method == "GET":
        user_id = request.query_params.get("user_id")

        if not is_valid_uuid(user_id):
            return Response(
                data={"error message": "user_id is not valid uuid"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_user_by_id(user_id)

        if not user:
            return Response(
                data={"error message": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        sent_requests = get_sent_requests(user)
        sent_requests_serializer = FriendshipRequestSerializer(sent_requests, many=True)
        sent_requests_list = get_requests_list(user_id, sent_requests_serializer.data)

        received_requests = get_received_requests(user)
        received_requests_serializer = FriendshipRequestSerializer(received_requests, many=True)
        received_requests_list = get_requests_list(user_id, received_requests_serializer.data)

        return Response(
            data={"user sent request to": sent_requests_list,
                  "user received request from": received_requests_list},
            status=status.HTTP_200_OK
        )


@api_view(["GET"])
def GetUserFriendsView(request):
    if request.method == "GET":
        user_id = request.query_params.get("user_id")

        if not is_valid_uuid(user_id):
            return Response(
                data={"error message": "User identifier is not valid uuid"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_user_by_id(user_id)

        if not user:
            return Response(
                data={"error message": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        friends = get_user_friends(user)
        serializer = FriendSerializer(friends, many=True)
        friends_list = get_friends_list(user_id, serializer.data)

        return Response(
            data={"User's friends": friends_list},
            status=status.HTTP_200_OK
        )


@api_view(["GET"])
def GetFriendshipStatusView(request):
    if request.method == "GET":
        user_1_id = request.query_params.get("user_1_id")
        user_2_id = request.query_params.get("user_2_id")

        if not is_valid_uuid(user_1_id) or not is_valid_uuid(user_2_id):
            return Response(
                data={"error message": "User identifier is not valid uuid"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user_1_id == user_2_id:
            return Response(
                data={"error message": "User identifiers are the same"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_1 = get_user_by_id(user_1_id)

        if not user_1:
            return Response(
                data={"error message": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        user_2 = get_user_by_id(user_2_id)

        if not user_2:
            return Response(
                data={"error message": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        friendship_status = get_status(user_1, user_2)

        if friendship_status == "friends":
            response_message = "user_1 and user_2 are friends"
        elif friendship_status == "the request sent by the current user":
            response_message = "user_1 sent friendship request to user_2"
        elif friendship_status == "the request is received by the current user":
            response_message = "user_1 received the request from user_2"
        else:
            response_message = "no friendship"

        return Response(
            data={"status": response_message},
            status=status.HTTP_200_OK
        )


@api_view(["DELETE"])
def RemoveFromFriendsView(request):
    if request.method == "DELETE":
        user_id = request.query_params.get("user_id")
        friend_id = request.query_params.get("friend_id")

        if not is_valid_uuid(user_id) or not is_valid_uuid(friend_id):
            return Response(
                data={"error message": "User identifier is not valid uuid"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user_id == friend_id:
            return Response(
                data={"error message": "User identifiers are the same"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_user_by_id(user_id)

        if not user:
            return Response(
                data={"error message": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        friend = get_user_by_id(friend_id)

        if not friend:
            return Response(
                data={"error message": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        remove_from_friends(user, friend)
        clear_friendship_requests(user, friend)

        return Response(
            data={"message": "Removal from friends was successful"},
            status=status.HTTP_200_OK
        )