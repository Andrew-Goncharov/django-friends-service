from typing import List, OrderedDict
from uuid import UUID

from ..models import User, Friend, FriendshipRequest


class FriendshipStatus:
    FRIENDS = "friends"
    NOT_FRIENDS = "not_friends"
    REQUEST_SENT = "request_sent"
    REQUEST_RECEIVED = "request_received"


def get_friends_list(user_id: UUID, data: List[OrderedDict]) -> List[str]:
    friends_list = []

    for row in data:
        friend_1_id = row["friend_1"]
        friend_2_id = row["friend_2"]
        if friend_1_id != user_id:
            friends_list.append(str(friend_1_id))
        else:
            friends_list.append(str(friend_2_id))

    return friends_list


def already_friends(user_1: User, user_2: User) -> bool:
    statement_1 = Friend.objects.filter(friend_1=user_1, friend_2=user_2).exists()
    statement_2 = Friend.objects.filter(friend_1=user_2, friend_2=user_1).exists()
    return statement_1 or statement_2


def get_status(user_1: User, user_2: User) -> str:
    if Friend.objects.filter(friend_1=user_1, friend_2=user_2).exists() or \
            Friend.objects.filter(friend_1=user_2, friend_2=user_1).exists():
        return FriendshipStatus.FRIENDS
    elif FriendshipRequest.objects.filter(sender=user_1, receiver=user_2).exists():
        return FriendshipStatus.REQUEST_SENT
    elif FriendshipRequest.objects.filter(sender=user_2, receiver=user_1).exists():
        return FriendshipStatus.REQUEST_RECEIVED
    else:
        return FriendshipStatus.NOT_FRIENDS


def get_user_friends(user: User) -> Friend:
    friends_1 = Friend.objects.filter(friend_1=user).all()
    friends_2 = Friend.objects.filter(friend_2=user).all()
    return (friends_1 | friends_2).distinct()


def remove_from_friends(user: User, friend: User):
    Friend.objects.filter(friend_1=user, friend_2=friend).delete()
    Friend.objects.filter(friend_1=friend, friend_2=user).delete()