import uuid

from django.db import models


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    username = models.CharField(max_length=20, unique=True)


class FriendshipRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    STATUS_CHOICES = (
        ("P", "Pending"),
        ("A", "Accepted"),
        ("R", "Rejected"),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="P")


class Friend(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    friend_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_1")
    friend_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_2")
