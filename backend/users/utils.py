from typing import Optional, List, OrderedDict
from uuid import UUID

from .models import User, Friend, FriendshipRequest


def accept_both_requests(user_1: User, user_2: User) -> None:
    request_1 = FriendshipRequest.objects.filter(sender=user_1, receiver=user_2).get()
    request_2 = FriendshipRequest.objects.filter(sender=user_1, receiver=user_2).get()
    if request_1.status != "P" or request_2.status != "P":
        raise ValueError("Cannot accept non-pending friendship request")
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


def user_exists(id: UUID) -> bool:
    return User.objects.filter(id=id).exists()


def request_exists(sender: User, receiver: User) -> bool:
    return FriendshipRequest.objects.filter(sender=sender, receiver=receiver).exists()


def get_user_by_id(id: UUID) -> User:
    return User.objects.filter(id=id).first()


def get_friendship_request(sender: UUID, receiver: UUID) -> Optional[FriendshipRequest]:
    return FriendshipRequest.objects.filter(sender=sender, receiver=receiver).first()


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


def already_friends(user_1: User, user_2: User) -> bool:
    statement_1 = Friend.objects.filter(friend_1=user_1, friend_2=user_2).exists()
    statement_2 = Friend.objects.filter(friend_1=user_2, friend_2=user_1).exists()
    return statement_1 or statement_2


def is_valid_uuid(value) -> bool:
    try:
        UUID(str(value))
        return True
    except ValueError:
        return False


def get_status(user_1: User, user_2: User) -> str:
    if user_1 == user_2:
        return "the same user"
    elif Friend.objects.filter(friend_1=user_1, friend_2=user_2).exists() or \
            Friend.objects.filter(friend_1=user_2, friend_2=user_1).exists():
        return "friends"
    elif FriendshipRequest.objects.filter(sender=user_1, receiver=user_2):
        return "the request sent by the current user"
    elif FriendshipRequest.objects.filter(sender=user_2, receiver=user_1):
        return "the request is received by the current user"
    else:
        return "no friendship"


def get_friendship_status(user_1: User, user_2: User) -> str:
    if user_1 == user_2:
        return "the same user"
    elif Friend.objects.filter(friend_1=user_1, friend_2=user_2).exists() or \
            Friend.objects.filter(friend_1=user_2, friend_2=user_1).exists():
        return "friends"
    elif FriendshipRequest.objects.filter(sender=user_1, receiver=user_2, status="A").exists() or \
            FriendshipRequest.objects.filter(sender=user_2, receiver=user_1, status="A").exists():
        return "request accepted"
    elif FriendshipRequest.objects.filter(sender=user_1, receiver=user_2, status="P").exists() or \
            FriendshipRequest.objects.filter(sender=user_2, receiver=user_1, status="P").exists():
        return "request pending"
    elif FriendshipRequest.objects.filter(sender=user_1, receiver=user_2, status="R").exists() or \
            FriendshipRequest.objects.filter(sender=user_2, receiver=user_1, status="R").exists():
        return "request rejected"
    else:
        return "no friendship"


def create_friendship_request(sender: User, receiver: User) -> None:
    if sender == receiver:
        raise ValueError("Cannot send friend request to yourself")
    elif request_exists(sender, receiver):
        raise ValueError("FriendshipRequest already exists")
    elif already_friends(sender, receiver):
        raise ValueError("Current users are already friends")
    # elif get_friendship_status(sender, receiver) != "no friendship":
    #     raise ValueError("Friendship or FriendshipRequest already exists")
    else:
        FriendshipRequest.objects.create(sender=sender, receiver=receiver)


def accept_friendship_request(request: FriendshipRequest) -> None:
    if request.status != "P":
        raise ValueError("Cannot accept non-pending friendship request")
    else:
        Friend.objects.create(friend_1=request.sender, friend_2=request.receiver)
        request.status = "A"
        request.save()


def reject_friendship_request(request: FriendshipRequest) -> None:
    if request.status != "P":
        raise ValueError("Cannot reject non-pending request")
    else:
        request.status = "R"
        request.save()


def get_sent_requests(user: User) -> FriendshipRequest:
    return FriendshipRequest.objects.filter(sender=user).all()


def get_received_requests(user: User) -> FriendshipRequest:
    return FriendshipRequest.objects.filter(receiver=user).all()


def get_user_friends(user: User) -> Friend:
    friends_1 = Friend.objects.filter(friend_1=user).all()
    friends_2 = Friend.objects.filter(friend_2=user).all()
    return (friends_1 | friends_2).distinct()


def remove_from_friends(user: User, friend: User):
    Friend.objects.filter(friend_1=user, friend_2=friend).delete()
    Friend.objects.filter(friend_1=friend, friend_2=user).delete()


def clear_friendship_requests(user: User, friend: User):
    FriendshipRequest.objects.filter(sender=user, receiver=friend).delete()
    FriendshipRequest.objects.filter(sender=friend, receiver=user).delete()
