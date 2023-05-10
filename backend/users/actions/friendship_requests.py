from typing import Optional, List, OrderedDict
from uuid import UUID

from rest_framework.exceptions import ValidationError

from ..actions.friendship import already_friends
from ..models import User, FriendshipRequest, Friend


def accept_both_requests(user_1: User, user_2: User) -> None:
    request_1 = FriendshipRequest.objects.filter(sender=user_1, receiver=user_2).get()
    request_2 = FriendshipRequest.objects.filter(sender=user_1, receiver=user_2).get()
    if request_1.status != "P" or request_2.status != "P":
        raise ValidationError("Cannot accept non-pending friendship request")
    else:
        Friend.objects.create(friend_1=user_1, friend_2=user_2)
        request_1.status = "A"
        request_1.save()
        request_2.status = "A"
        request_2.save()


def requests_from_both_users_exist(user_1: User, user_2: User) -> bool:
    statement_1 = FriendshipRequest.objects.filter(sender=user_1, receiver=user_2).exists()
    statement_2 = FriendshipRequest.objects.filter(sender=user_2, receiver=user_1).exists()
    return statement_1 and statement_2


def request_exists(sender: User, receiver: User) -> bool:
    return FriendshipRequest.objects.filter(sender=sender, receiver=receiver).exists()


def get_friendship_request(sender: UUID, receiver: UUID) -> Optional[FriendshipRequest]:
    return FriendshipRequest.objects.filter(sender=sender, receiver=receiver).first()


def get_requests_list(user_id: UUID, data: List[OrderedDict]) -> List[str]:
    requests_list = []

    for row in data:
        sender_id = row["sender"]
        receiver_id = row["receiver"]

        if sender_id != user_id:
            requests_list.append(sender_id)
        else:
            requests_list.append(receiver_id)

    return requests_list


def create_friendship_request(sender: User, receiver: User) -> None:
    if sender == receiver:
        raise ValidationError("Cannot send friend request to yourself")
    elif request_exists(sender, receiver):
        raise ValidationError("FriendshipRequest already exists")
    elif already_friends(sender, receiver):
        raise ValidationError("Current users are already friends")
    else:
        FriendshipRequest.objects.create(sender=sender, receiver=receiver)


def accept_friendship_request(request: FriendshipRequest) -> None:
    if request.status != "P":
        raise ValidationError("Cannot accept non-pending friendship request")
    else:
        Friend.objects.create(friend_1=request.sender, friend_2=request.receiver)
        request.status = "A"
        request.save()


def reject_friendship_request(request: FriendshipRequest) -> None:
    if request.status != "P":
        raise ValidationError("Cannot reject non-pending request")
    else:
        request.status = "R"
        request.save()


def get_sent_requests(user: User) -> FriendshipRequest:
    return FriendshipRequest.objects.filter(sender=user).all()


def get_received_requests(user: User) -> FriendshipRequest:
    return FriendshipRequest.objects.filter(receiver=user).all()


def clear_friendship_requests(user: User, friend: User):
    FriendshipRequest.objects.filter(sender=user, receiver=friend).delete()
    FriendshipRequest.objects.filter(sender=friend, receiver=user).delete()