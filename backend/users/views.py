from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import UserSerializer, FriendshipRequestSerializer, ProcessFriendshipRequestSerializer, \
    FriendSerializer
from .actions import user_exists, get_user_by_id, create_friendship_request, get_friendship_request, \
    accept_friendship_request, reject_friendship_request, is_valid_uuid, get_status, \
    get_user_friends, get_friends_list, get_sent_requests, get_received_requests, get_requests_list, \
    remove_from_friends, clear_friendship_requests, requests_from_both_users_exist, accept_both_requests


@api_view(["POST"])
def create_user_view(request):
    data = request.data
    serializer = UserSerializer(data=data)

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(
        status=status.HTTP_201_CREATED
    )


@api_view(["POST"])
def create_friendship_request_view(request):
    data = request.data
    serializer = FriendshipRequestSerializer(data=data)

    serializer.is_valid(raise_exception=True)
    sender_id = serializer.data["sender"]
    receiver_id = serializer.data["receiver"]

    sender = get_user_by_id(sender_id)
    receiver = get_user_by_id(receiver_id)
    create_friendship_request(sender, receiver)

    if requests_from_both_users_exist(sender, receiver):
        accept_both_requests(sender, receiver)

    return Response(
        data={"message": "FriendshipRequest successfully created"},
        status=status.HTTP_201_CREATED
    )


@api_view(["POST"])
def process_friendship_request_view(request):
    data = request.data

    serializer = ProcessFriendshipRequestSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    sender = serializer.data["sender"]
    receiver = serializer.data["receiver"]
    action = serializer.data["action"]

    request = get_friendship_request(sender, receiver)

    if not request:
        raise NotFound("FriendshipRequest not found")

    if action == "accept":
        accept_friendship_request(request)
    elif action == "reject":
        reject_friendship_request(request)

    return Response(
        status=status.HTTP_200_OK
    )


@api_view(["GET"])
def get_friendship_requests_view(request):
    user_id = request.query_params.get("user_id")

    if not is_valid_uuid(user_id):
        raise ValidationError("user_id is not valid uuid")

    user = get_user_by_id(user_id)

    if not user:
        raise NotFound("User not found")

    sent_requests = get_sent_requests(user)
    sent_requests_serializer = FriendshipRequestSerializer(sent_requests, many=True)
    sent_requests_list = get_requests_list(user_id, sent_requests_serializer.data)

    received_requests = get_received_requests(user)
    received_requests_serializer = FriendshipRequestSerializer(received_requests, many=True)
    received_requests_list = get_requests_list(user_id, received_requests_serializer.data)

    return Response(
        data={"sent_requests": sent_requests_list,
              "received_requests": received_requests_list},
        status=status.HTTP_200_OK
    )


@api_view(["GET"])
def get_user_friends_view(request):
    user_id = request.query_params.get("user_id")

    if not is_valid_uuid(user_id):
        raise ValidationError("user_id is not valid uuid")

    user = get_user_by_id(user_id)

    if not user:
        raise NotFound("User not found")

    friends = get_user_friends(user)
    serializer = FriendSerializer(friends, many=True)
    friends_list = get_friends_list(user_id, serializer.data)

    return Response(
        data={"friends": friends_list},
        status=status.HTTP_200_OK
    )


@api_view(["GET"])
def get_friendship_status_view(request):
    user_id_1 = request.query_params.get("user_id_1")
    user_id_2 = request.query_params.get("user_id_2")

    if not is_valid_uuid(user_id_1):
        raise ValidationError("user_id_1 is not valid uuid")

    if not is_valid_uuid(user_id_2):
        raise ValidationError("user_id_2 is not valid uuid")

    if user_id_1 == user_id_2:
        raise ValidationError("User identifiers are the same")

    user_1 = get_user_by_id(user_id_1)
    if not user_1:
        raise NotFound("User not found")

    user_2 = get_user_by_id(user_id_2)
    if not user_2:
        raise NotFound("User not found")

    friendship_status = get_status(user_1, user_2)

    return Response(
        data={"status": friendship_status},
        status=status.HTTP_200_OK
    )


@api_view(["DELETE"])
def remove_from_friends_view(request):
    user_id = request.query_params.get("user_id")
    friend_id = request.query_params.get("friend_id")

    if not is_valid_uuid(user_id):
        raise ValidationError("user_id is not valid uuid")

    if not is_valid_uuid(friend_id):
        raise ValidationError("friend_id is not valid uuid")

    if user_id == friend_id:
        raise ValidationError("User identifiers are the same")

    user = get_user_by_id(user_id)
    if not user:
        raise NotFound("User not found")

    friend = get_user_by_id(friend_id)
    if not friend:
        raise NotFound("User not found")

    remove_from_friends(user, friend)
    clear_friendship_requests(user, friend)

    return Response(
        status=status.HTTP_200_OK
    )