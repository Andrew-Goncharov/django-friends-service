from django.contrib import admin

from .models import User, FriendshipRequest, Friend

admin.site.register(User)
admin.site.register(FriendshipRequest)
admin.site.register(Friend)
